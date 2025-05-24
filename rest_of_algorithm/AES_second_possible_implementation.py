import numpy as np 
import os
from hashlib import pbkdf2_hmac
from hmac import new as new_hmac, compare_digest


# Calculates the multiplicative inverse of x in GF(2^8) using modular arithmetic with the irreducible polynomial 0x11B used in AES. 
def gf256_inv(x):
    if x == 0:
        return 0
    return pow(x, 254, 0x11B)

# This function applies the affine transformation (bitwise operations) as used in AES. 
# It essentially performs a series of bit shifts and XORs to make the S-box non-linear.
def affine_transform(x):
    transformed = x ^ (x << 1) ^ (x << 2) ^ (x << 3) ^ (x << 4) ^ 0x63  
    return transformed

# Generated the s-box
def generate_sbox():
    sbox = []
    for i in range(256):
        inv = gf256_inv(i)
        transformed = affine_transform(inv)
        sbox.append(transformed & 0xFF)  # Mask to keep the result within byte range (0-255)
    return sbox

def generate_inverse_sbox(sbox):
    inverse_sbox = [0] * 256
    for i, val in enumerate(sbox):
        inverse_sbox[val] = i
    return inverse_sbox


# Generate S-box and its inverse
s_box = generate_sbox()
inv_s_box = generate_inverse_sbox(s_box)


# Converts a byte string into a 4x4 matrix (list of lists), where each inner list represents a row.
def bytes2matrix(input):
    if len(input) % 4 != 0:
        raise ValueError("Input length must be a multiple of 4.")
    
    matrix = [list(input[i:i+4]) for i in range(0, len(input), 4)]
    
    return matrix

# Converts a 4x4 matrix of bytes (list of lists) back into a byte string.
def matrix2bytes(matrix):
    # Flatten the matrix and convert to a bytes object
    flattened = [byte for row in matrix for byte in row]
    
    return bytes(flattened)



# Perform bitwise XOR between two byte sequences.
def XORbytes(x, y):
    # Ensure the byte sequences are of the same length
    if len(x) != len(y):
        raise ValueError("The byte sequences must have the same length.")
    
    # Perform the XOR operation byte by byte and return the result as a bytes object
    return bytes(i ^ j for i, j in zip(x, y))

# Increment a byte sequence by 1, handling overflow at the byte level.
def incBytes(x):
    # Convert input bytes to a list of integers
    out = list(x)
    
    # Iterate through the byte sequence in reverse order
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:  # Check for overflow
            out[i] = 0  # Reset to 0 (carry over)
        else:
            out[i] += 1  # Increment the byte and exit the loop
            break
    
    # Return the modified byte sequence as bytes
    return bytes(out)


# Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
# If the input is already a multiple of 16 bytes, an entire 16-byte block 
# of padding is added.
def pad(input_data):
    # Calculate padding length (ensuring it's between 1 and 16)
    padding_len = 16 - (len(input_data) % 16)
    # Create the padding block (repeating the padding_len byte)
    padding = bytes([padding_len] * padding_len)
    
    return input_data + padding

# removes padding again
def unpad(input_data):
    if len(input_data) == 0:
        raise ValueError("Input data is empty, padding cannot be removed.")
    
    padding_len = input_data[-1]

    # Ensure the padding length is valid and does not exceed the block size (16 bytes)
    if padding_len < 1 or padding_len > 16:
        raise ValueError(f"Invalid padding length: {padding_len}")
    
    # Extract the padding part and the message part
    message, padding = input_data[:-padding_len], input_data[-padding_len:]

    # Ensure all padding bytes are equal to the padding length
    if any(p != padding_len for p in padding):
        raise ValueError("Invalid padding bytes detected. Padding is corrupted.")
    
    return message



# Split blocks if our message is longer than 16 byts
def split_blocks(message, block_size=16, require_padding=True):
    # If padding is required, pad the message to a multiple of block_size
    if require_padding:
        padding_len = (block_size - len(message) % block_size) % block_size
        if padding_len:
            message += bytes([padding_len] * padding_len)

    # Ensure the message length is now a multiple of block_size
    if len(message) % block_size != 0:
        raise ValueError(f"Message length {len(message)} is not a multiple of block size {block_size}")

    # Split the message into blocks of the specified size
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]




def sub_bytes(state):
    # Apply the S-box transformation to every byte in the state
    for row in range(4):
        for col in range(4):
            state[row][col] = s_box[state[row][col]]


def inv_sub_bytes(state):
    # Apply the inverse S-box transformation to every byte in the state
    for row in range(4):
        for col in range(4):
            state[row][col] = inv_s_box[state[row][col]]


def shift_rows(state):
    # Shift rows cyclically to the left
    state[1] = state[1][1:] + state[1][:1] 
    state[2] = state[2][2:] + state[2][:2] 
    state[3] = state[3][3:] + state[3][:3]


def inv_shift_rows(state):
    # Perform inverse of the ShiftRows operation by shifting rows right
    # Each row is cyclically rotated to the right
    state[1] = [state[1][3], state[1][0], state[1][1], state[1][2]]
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    state[3] = [state[3][1], state[3][2], state[3][3], state[3][0]]

# This function applies the XOR operation between the AES state matrix and the
# round key matrix. It performs the operation in place, modifying the state.
def add_round_key(state, key):
    # Apply XOR between state and key for each byte in the 4x4 matrix
    for row in range(4):
        for col in range(4):
            state[row][col] ^= key[row][col]



#   This function takes a byte and performs the multiplication by 2 in the finite field
# GF(2^8), which is done by shifting the byte left by 1 bit and reducing modulo 
# the irreducible polynomial if the leftmost bit is set (0x80).
def xtime(byte):
    # If the most significant bit (0x80) is set, apply the irreducible polynomial 0x1B
    if byte & 0x80:
        return ((byte << 1) ^ 0x1B) & 0xFF
    else:
        # Just shift the byte left by 1 bit, as it doesn't overflow into the irreducible polynomial
        return byte << 1

def mix_single_column(column):
    # XOR of all four bytes in the column (this helps with the diffusion step)
    t = column[0] ^ column[1] ^ column[2] ^ column[3]

    # Store the original value of the first byte for later use
    u = column[0]

    # Update each byte by XORing it with 't' and the xtime result of the XOR with the next byte
    column[0] ^= t ^ xtime(column[0] ^ column[1])  # Update first byte using xtime(a[0] ^ a[1])
    column[1] ^= t ^ xtime(column[1] ^ column[2])  # Update second byte using xtime(a[1] ^ a[2])
    column[2] ^= t ^ xtime(column[2] ^ column[3])  # Update third byte using xtime(a[2] ^ a[3])
    column[3] ^= t ^ xtime(column[3] ^ u)          # Update fourth byte using xtime(a[3] ^ u)


def mix_columns(state):
    # Apply mix_single_column to each column in the state matrix (4 columns in total)
    for column in state:
        mix_single_column(column)


def inv_mix_columns(state):
    # Process each column (loop over 4 columns)
    for i in range(4):
        # Compute u and v for the column based on XOR and xtime (multiply by 2 in GF(2^8))
        u = xtime(xtime(state[i][0] ^ state[i][2]))  # u is based on s[i][0] and s[i][2]
        v = xtime(xtime(state[i][1] ^ state[i][3]))  # v is based on s[i][1] and s[i][3]

        # Reverse the MixColumns effect by XORing with u and v
        state[i][0] ^= u  
        state[i][1] ^= v 
        state[i][2] ^= u 
        state[i][3] ^= v

    # Call mix_columns(s) to finalize the inverse transformation
    mix_columns(state)
    
    
    
r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)




class AES:
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}
    def __init__(self, master_key):
        # Initializes the object with a given key.
        
        assert len(master_key) in AES.rounds_by_key_size
        self.n_rounds = AES.rounds_by_key_size[len(master_key)]
        self._key_matrices = self._expand_key(master_key)

    # Expands and returns a list of key matrices for the given master_key.
    def _expand_key(self, master_key):
        
        
        # Initialize round keys with raw key material.
        key_columns = bytes2matrix(master_key)
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            # Copy previous word.
            word = list(key_columns[-1])

            # Perform schedule_core once every "row".
            if len(key_columns) % iteration_size == 0:
                # Circular shift.
                word.append(word.pop(0))
                # Map to S-BOX.
                word = [s_box[b] for b in word]
                # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                # Run word through S-box in the fourth iteration when using a
                # 256-bit key.
                word = [s_box[b] for b in word]

            # XOR with equivalent word from previous iteration.
            word = XORbytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        # Group key words in 4x4 byte matrices.
        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
    
    # Encrypts a single block of 16 byte long plaintext.
    def encrypt_block(self, plaintext):
        
        assert len(plaintext) == 16

        plain_state = bytes2matrix(plaintext)

        add_round_key(plain_state, self._key_matrices[0])

        for i in range(1, self.n_rounds):
            sub_bytes(plain_state)
            shift_rows(plain_state)
            mix_columns(plain_state)
            add_round_key(plain_state, self._key_matrices[i])

        sub_bytes(plain_state)
        shift_rows(plain_state)
        add_round_key(plain_state, self._key_matrices[-1])

        return matrix2bytes(plain_state)

    # Decrypts a single block of 16 byte long ciphertext.
    def decrypt_block(self, ciphertext):
        assert len(ciphertext) == 16

        cipher_state = bytes2matrix(ciphertext)

        add_round_key(cipher_state, self._key_matrices[-1])
        inv_shift_rows(cipher_state)
        inv_sub_bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            add_round_key(cipher_state, self._key_matrices[i])
            inv_mix_columns(cipher_state)
            inv_shift_rows(cipher_state)
            inv_sub_bytes(cipher_state)

        add_round_key(cipher_state, self._key_matrices[0])

        return matrix2bytes(cipher_state)
    
    # Encrypts `plaintext` using CTR mode with the given nonce/IV.
    # Ensures padding of the message.
    def encrypt_ctr(self, plaintext, iv):
        assert len(iv) == 16

        # Padding plaintext to ensure it's a multiple of 16 bytes
        blocks = []
        nonce = iv
        padded_plaintext = pad(plaintext)  # Pad the plaintext here to a multiple of 16 bytes
        for plaintext_block in split_blocks(padded_plaintext, require_padding=False):  # Now, padding is handled
            # CTR mode encrypt: plaintext_block XOR encrypt(nonce)
            block = XORbytes(plaintext_block, self.encrypt_block(nonce))
            blocks.append(block)
            nonce = incBytes(nonce)

        return b''.join(blocks)

    def decrypt_ctr(self, ciphertext, iv):
        assert len(iv) == 16

        blocks = []
        nonce = iv
        for ciphertext_block in split_blocks(ciphertext, require_padding=False):
            # CTR mode decrypt: ciphertext XOR encrypt(nonce)
            block = XORbytes(ciphertext_block, self.encrypt_block(nonce))
            blocks.append(block)
            nonce = incBytes(nonce)

        return b''.join(blocks)
    
    

AES_KEY_SIZE = 16
HMAC_KEY_SIZE = 16
IV_SIZE = 16

SALT_SIZE = 16
HMAC_SIZE = 32


# Stretches the password and extracts an AES key, an HMAC key and an AES initialization vector.
def get_key_iv(password, salt, workload=100000):
    stretched = pbkdf2_hmac('sha256', password, salt, workload, AES_KEY_SIZE + IV_SIZE + HMAC_KEY_SIZE)
    aes_key, stretched = stretched[:AES_KEY_SIZE], stretched[AES_KEY_SIZE:]
    hmac_key, stretched = stretched[:HMAC_KEY_SIZE], stretched[HMAC_KEY_SIZE:]
    iv = stretched[:IV_SIZE]
    return aes_key, hmac_key, iv


def encrypt(key, plaintext, workload=100000):

    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    salt = os.urandom(SALT_SIZE)
    key, hmac_key, iv = get_key_iv(key, salt, workload)
    ciphertext = AES(key).encrypt_ctr(plaintext, iv)
    hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
    assert len(hmac) == HMAC_SIZE

    return hmac + salt + ciphertext


def decrypt(key, ciphertext, workload=100000):
    if isinstance(key, str):
        key = key.encode('utf-8')

    # Ensure the ciphertext is long enough to contain HMAC, salt, and data
    if len(ciphertext) < (SALT_SIZE + HMAC_SIZE):
        raise ValueError("Ciphertext is too short to contain HMAC and salt.")
    
    # Extract the HMAC, salt, and the actual ciphertext
    hmac, ciphertext = ciphertext[:HMAC_SIZE], ciphertext[HMAC_SIZE:]
    salt, ciphertext = ciphertext[:SALT_SIZE], ciphertext[SALT_SIZE:]

    # Derive the AES key, HMAC key, and IV from the password and salt using PBKDF2
    key, hmac_key, iv = get_key_iv(key, salt, workload)

    # Verify the integrity of the ciphertext using HMAC
    expected_hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
    if not compare_digest(hmac, expected_hmac):
        raise ValueError("HMAC verification failed: Ciphertext may have been tampered with.")

    # Decrypt the ciphertext using AES CTR mode
    try:
        decrypted_data = AES(key).decrypt_ctr(ciphertext, iv)
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

    # Remove padding after decryption (if any)
    try:
        return unpad(decrypted_data)
    except ValueError:
        raise ValueError("Padding error: Unable to remove padding from decrypted data.")
    
    
    

def main():
    key = "mypassword"
    input = "This is very secret message."

    # Encrypt the plaintext
    encrypted_data = encrypt(key, input)
    print("Encrypted:", encrypted_data)

    decrypted_data = decrypt(key, encrypted_data)
    print("Decrypted:", decrypted_data)

if __name__ == '__main__':
    main()