# Python program to illustrate ElGamal encryption
import random
from math import gcd

def power(a, b, c):
    """Efficient modular exponentiation"""
    if b == 0:
        return 1
    elif b == 1:
        return a % c
    else:
        return pow(a, b, c)  # Python's built-in pow is more efficient

def gen_key(q):
    """Generate a random key coprime to q"""
    # Use smaller range for practical purposes
    key = random.randint(2, min(q-1, 10000))
    while gcd(q, key) != 1:
        key = random.randint(2, min(q-1, 10000))
    return key

def generate_elgamal_keys(p=None, g=None):
    """Generate ElGamal public and private key pair"""
    # Use manageable prime numbers for demonstration
    if p is None:
        # Using a known safe prime for demonstration
        p = 2357  # A reasonably sized prime
    if g is None:
        g = 2  # A common generator
    
    # Generate private key
    private_key = gen_key(p)
    
    # Generate public key components
    public_key_h = power(g, private_key, p)
    
    return {
        'private_key': private_key,
        'public_key': (p, g, public_key_h),
        'p': p,
        'g': g,
        'h': public_key_h
    }

def elgamal_encrypt(message, public_key_tuple):
    """
    Encrypt message using ElGamal encryption
    public_key_tuple = (p, g, h)
    Returns (ciphertext, ephemeral_key)
    """
    p, g, h = public_key_tuple
    
    # Convert message to bytes if it's a string
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
    
    # Generate ephemeral key k
    k = gen_key(p)
    
    # Calculate c1 = g^k mod p
    c1 = power(g, k, p)
    
    # Calculate s = h^k mod p (shared secret)
    s = power(h, k, p)
    
    # Encrypt each byte
    ciphertext = []
    for byte_val in message_bytes:
        # c2 = m * s mod p
        encrypted_byte = (byte_val * s) % p
        ciphertext.append(encrypted_byte)
    
    return ciphertext, c1

def elgamal_decrypt(ciphertext, c1, private_key, p):
    """
    Decrypt ElGamal ciphertext
    ciphertext: list of encrypted integers
    c1: ephemeral public key (g^k mod p)
    private_key: receiver's private key
    p: prime modulus
    """
    # Calculate s = c1^private_key mod p = (g^k)^a mod p = g^(ka) mod p
    s = power(c1, private_key, p)
    
    # Calculate modular inverse of s
    s_inv = power(s, p - 2, p)  # Using Fermat's little theorem: s^(p-1) ≡ 1 (mod p)
    
    # Decrypt each encrypted byte
    decrypted_bytes = []
    for encrypted_byte in ciphertext:
        # m = c2 * s^(-1) mod p
        original_byte = (encrypted_byte * s_inv) % p
        if original_byte < 256:  # Valid ASCII/UTF-8 byte
            decrypted_bytes.append(original_byte)
    
    try:
        return bytes(decrypted_bytes).decode('utf-8')
    except UnicodeDecodeError:
        return bytes(decrypted_bytes).decode('utf-8', errors='ignore')

# Legacy functions for compatibility
def encrypt(msg, q, h, g):
    """Legacy encrypt function for backward compatibility"""
    public_key = (q, g, h)
    ciphertext, c1 = elgamal_encrypt(msg, public_key)
    return ciphertext, c1

def decrypt(en_msg, p, key, q):
    """Legacy decrypt function for backward compatibility"""
    return elgamal_decrypt(en_msg, p, key, q)

def main():
    """Demonstration of ElGamal encryption"""
    
    # Generate keys
    keys = generate_elgamal_keys()
    print(f"Generated keys:")
    print(f"Private key: {keys['private_key']}")
    print(f"Public key (p, g, h): {keys['public_key']}")
    print(f"p: {keys['p']}, g: {keys['g']}, h: {keys['h']}")
    print()
    
    # Message to encrypt
    message = "Hello ElGamal!"
    print(f"Original message: {message}")
    
    # Encrypt
    ciphertext, c1 = elgamal_encrypt(message, keys['public_key'])
    print(f"Encrypted message: {ciphertext}")
    print(f"Ephemeral key (c1): {c1}")
    
    # Decrypt
    decrypted_message = elgamal_decrypt(ciphertext, c1, keys['private_key'], keys['p'])
    print(f"Decrypted message: {decrypted_message}")
    
    # Verify
    print(f"Encryption successful: {message == decrypted_message}")

if __name__ == '__main__':
    main()
