
import base64

def rc4_encrypt_decrypt(data, key):
    """Core RC4 algorithm - works for both encryption and decryption"""
    # Convert key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Initialize S-box
    S = list(range(256))
    j = 0
    
    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    result = []
    
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream_byte = S[(S[i] + S[j]) % 256]
        result.append(byte ^ keystream_byte)
    
    return bytes(result)

def rc4_encrypt(plain_text, key):
    """Encrypt text using RC4 and return base64 encoded result"""
    try:
        encrypted_bytes = rc4_encrypt_decrypt(plain_text, key)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Encryption Error: {str(e)}")

def rc4_decrypt(cipher_text_base64, key):
    """Decrypt base64 encoded RC4 ciphertext"""
    try:
        encrypted_bytes = base64.b64decode(cipher_text_base64)
        decrypted_bytes = rc4_encrypt_decrypt(encrypted_bytes, key)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Decryption Error: {str(e)}")