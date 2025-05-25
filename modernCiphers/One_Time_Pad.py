def otp_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts the plaintext using the One-Time Pad method.
    Assumes plaintext and key are uppercase and alphabetic only.
    """
    if len(plaintext) != len(key):
        raise ValueError("Key must be the same length as plaintext")

    ciphertext = ""
    for p, k in zip(plaintext, key):
        c = (ord(p) - ord('A') + ord(k) - ord('A')) % 26
        ciphertext += chr(c + ord('A'))
    return ciphertext

def otp_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts the ciphertext using the One-Time Pad method.
    Assumes ciphertext and key are uppercase and alphabetic only.
    """
    if len(ciphertext) != len(key):
        raise ValueError("Key must be the same length as ciphertext")

    plaintext = ""
    for c, k in zip(ciphertext, key):
        p = (ord(c) - ord('A') - (ord(k) - ord('A'))) % 26
        plaintext += chr(p + ord('A'))
    return plaintext

# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    plain_text = "HELLO"
    key = "MONEY"

    encrypted = otp_encrypt(plain_text, key)
    print("Encrypted:", encrypted)

    decrypted = otp_decrypt(encrypted, key)
    print("Decrypted:", decrypted)
