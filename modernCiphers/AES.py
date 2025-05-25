import base64
import os
from hashlib import pbkdf2_hmac
from hmac import new as new_hmac, compare_digest

# AES Constants
AES_KEY_SIZE = 16  # 128-bit key
HMAC_KEY_SIZE = 16
IV_SIZE = 16
SALT_SIZE = 16
HMAC_SIZE = 32

# Generate S-box for AES
def gf256_inv(x):
    if x == 0:
        return 0
    return pow(x, 254, 0x11B)

def affine_transform(x):
    transformed = x ^ (x << 1) ^ (x << 2) ^ (x << 3) ^ (x << 4) ^ 0x63  
    return transformed

def generate_sbox():
    sbox = []
    for i in range(256):
        inv = gf256_inv(i)
        transformed = affine_transform(inv)
        sbox.append(transformed & 0xFF)
    return sbox

def generate_inverse_sbox(sbox):
    inverse_sbox = [0] * 256
    for i, val in enumerate(sbox):
        inverse_sbox[val] = i
    return inverse_sbox

# Generate S-box and its inverse
s_box = generate_sbox()
inv_s_box = generate_inverse_sbox(s_box)

# R-CON values for key expansion
r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

# Utility functions
def bytes2matrix(input_bytes):
    if len(input_bytes) % 4 != 0:
        raise ValueError("Input length must be a multiple of 4.")
    matrix = [list(input_bytes[i:i+4]) for i in range(0, len(input_bytes), 4)]
    return matrix

def matrix2bytes(matrix):
    flattened = [byte for row in matrix for byte in row]
    return bytes(flattened)

def XORbytes(x, y):
    if len(x) != len(y):
        raise ValueError("The byte sequences must have the same length.")
    return bytes(i ^ j for i, j in zip(x, y))

def incBytes(x):
    out = list(x)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)

def pad(input_data):
    padding_len = 16 - (len(input_data) % 16)
    padding = bytes([padding_len] * padding_len)
    return input_data + padding

def unpad(input_data):
    if len(input_data) == 0:
        raise ValueError("Input data is empty, padding cannot be removed.")
    
    padding_len = input_data[-1]
    if padding_len < 1 or padding_len > 16:
        raise ValueError(f"Invalid padding length: {padding_len}")
    
    message, padding = input_data[:-padding_len], input_data[-padding_len:]
    if any(p != padding_len for p in padding):
        raise ValueError("Invalid padding bytes detected. Padding is corrupted.")
    
    return message

def split_blocks(message, block_size=16, require_padding=True):
    if require_padding:
        padding_len = (block_size - len(message) % block_size) % block_size
        if padding_len:
            message += bytes([padding_len] * padding_len)

    if len(message) % block_size != 0:
        raise ValueError(f"Message length {len(message)} is not a multiple of block size {block_size}")

    return [message[i:i + block_size] for i in range(0, len(message), block_size)]

# AES operations
def sub_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = s_box[state[row][col]]

def inv_sub_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = inv_s_box[state[row][col]]

def shift_rows(state):
    state[1] = state[1][1:] + state[1][:1] 
    state[2] = state[2][2:] + state[2][:2] 
    state[3] = state[3][3:] + state[3][:3]

def inv_shift_rows(state):
    state[1] = [state[1][3], state[1][0], state[1][1], state[1][2]]
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    state[3] = [state[3][1], state[3][2], state[3][3], state[3][0]]

def add_round_key(state, key):
    for row in range(4):
        for col in range(4):
            state[row][col] ^= key[row][col]

def xtime(byte):
    if byte & 0x80:
        return ((byte << 1) ^ 0x1B) & 0xFF
    else:
        return byte << 1

def mix_single_column(column):
    t = column[0] ^ column[1] ^ column[2] ^ column[3]
    u = column[0]
    column[0] ^= t ^ xtime(column[0] ^ column[1])
    column[1] ^= t ^ xtime(column[1] ^ column[2])
    column[2] ^= t ^ xtime(column[2] ^ column[3])
    column[3] ^= t ^ xtime(column[3] ^ u)

def mix_columns(state):
    for column in state:
        mix_single_column(column)

def inv_mix_columns(state):
    for i in range(4):
        u = xtime(xtime(state[i][0] ^ state[i][2]))
        v = xtime(xtime(state[i][1] ^ state[i][3]))
        state[i][0] ^= u  
        state[i][1] ^= v 
        state[i][2] ^= u 
        state[i][3] ^= v
    mix_columns(state)

class AES:
    def __init__(self, master_key):
        # Force AES-128 (16-byte key)
        if len(master_key) != 16:
            raise ValueError("AES-128 requires exactly 16 bytes (128 bits) key")
        
        self.n_rounds = 10  # AES-128 uses 10 rounds
        self._key_matrices = self._expand_key(master_key)

    def _expand_key(self, master_key):
        key_columns = bytes2matrix(master_key)
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            word = list(key_columns[-1])

            if len(key_columns) % iteration_size == 0:
                word.append(word.pop(0))
                word = [s_box[b] for b in word]
                word[0] ^= r_con[i]
                i += 1

            word = XORbytes(word, key_columns[-iteration_size])
            key_columns.append(word)

        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
    
    def encrypt_block(self, plaintext):
        if len(plaintext) != 16:
            raise ValueError("Block must be exactly 16 bytes")

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

    def decrypt_block(self, ciphertext):
        if len(ciphertext) != 16:
            raise ValueError("Block must be exactly 16 bytes")

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
    
    def encrypt_ctr(self, plaintext, iv):
        if len(iv) != 16:
            raise ValueError("IV must be exactly 16 bytes")

        blocks = []
        nonce = iv
        padded_plaintext = pad(plaintext)
        
        for plaintext_block in split_blocks(padded_plaintext, require_padding=False):
            block = XORbytes(plaintext_block, self.encrypt_block(nonce))
            blocks.append(block)
            nonce = incBytes(nonce)

        return b''.join(blocks)

    def decrypt_ctr(self, ciphertext, iv):
        if len(iv) != 16:
            raise ValueError("IV must be exactly 16 bytes")

        blocks = []
        nonce = iv
        
        for ciphertext_block in split_blocks(ciphertext, require_padding=False):
            block = XORbytes(ciphertext_block, self.encrypt_block(nonce))
            blocks.append(block)
            nonce = incBytes(nonce)

        return b''.join(blocks)

# Key derivation function
def get_key_iv(password, salt, workload=100000):
    stretched = pbkdf2_hmac('sha256', password, salt, workload, AES_KEY_SIZE + IV_SIZE + HMAC_KEY_SIZE)
    aes_key, stretched = stretched[:AES_KEY_SIZE], stretched[AES_KEY_SIZE:]
    hmac_key, stretched = stretched[:HMAC_KEY_SIZE], stretched[HMAC_KEY_SIZE:]
    iv = stretched[:IV_SIZE]
    return aes_key, hmac_key, iv

# Main encryption function (exported)
def aes_encrypt(plaintext, password):
    """
    Encrypt plaintext using AES-128 in CTR mode with HMAC authentication.
    Returns base64 encoded result.
    """
    try:
        # Convert inputs to bytes if they're strings
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        # Generate random salt
        salt = os.urandom(SALT_SIZE)
        
        # Derive keys and IV
        aes_key, hmac_key, iv = get_key_iv(password, salt)
        
        # Encrypt using AES-128 CTR mode
        ciphertext = AES(aes_key).encrypt_ctr(plaintext, iv)
        
        # Create HMAC for authentication
        hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
        
        # Combine HMAC + salt + ciphertext
        encrypted_data = hmac + salt + ciphertext
        
        # Return base64 encoded result
        return base64.b64encode(encrypted_data).decode('utf-8')
        
    except Exception as e:
        return f"Encryption Error: {str(e)}"

# Main decryption function (exported)
def aes_decrypt(encrypted_data_base64, password):
    """
    Decrypt base64 encoded AES-128 encrypted data.
    Verifies HMAC before decryption.
    """
    try:
        # Convert password to bytes if it's a string
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Decode base64
        encrypted_data = base64.b64decode(encrypted_data_base64)
        
        # Ensure the data is long enough to contain HMAC, salt, and ciphertext
        if len(encrypted_data) < (SALT_SIZE + HMAC_SIZE):
            raise ValueError("Encrypted data is too short to contain HMAC and salt.")
        
        # Extract components
        hmac = encrypted_data[:HMAC_SIZE]
        salt = encrypted_data[HMAC_SIZE:HMAC_SIZE + SALT_SIZE]
        ciphertext = encrypted_data[HMAC_SIZE + SALT_SIZE:]
        
        # Derive keys and IV
        aes_key, hmac_key, iv = get_key_iv(password, salt)
        
        # Verify HMAC
        expected_hmac = new_hmac(hmac_key, salt + ciphertext, 'sha256').digest()
        if not compare_digest(hmac, expected_hmac):
            raise ValueError("HMAC verification failed: Data may have been tampered with or wrong password.")
        
        # Decrypt using AES-128 CTR mode
        decrypted_data = AES(aes_key).decrypt_ctr(ciphertext, iv)
        
        # Remove padding
        plaintext = unpad(decrypted_data)
        
        # Return as string
        return plaintext.decode('utf-8')
        
    except Exception as e:
        raise ValueError(f"Decryption Error: {str(e)}")