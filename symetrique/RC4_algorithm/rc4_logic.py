import base64

def rc4(text, key):
    S = list(range(256))
    j = 0
    key_bytes = [ord(k) for k in key]  # clé sous forme de chaîne

    # KSA
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA
    i = j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))

    return ''.join(result)

def encrypt(plain_text, key):
    encrypted = rc4(plain_text, key)
    return base64.b64encode(encrypted.encode()).decode()

def decrypt(cipher_text_base64, key):
    try:
        decoded = base64.b64decode(cipher_text_base64.encode()).decode()
        return rc4(decoded, key)
    except Exception as e:
        return f"Erreur : {str(e)}"
