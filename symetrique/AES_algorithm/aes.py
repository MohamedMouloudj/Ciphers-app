import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY_FILE = "AES/aes_key.bin"

def save_key(key):
    """Save AES key to a file."""
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    """Load the AES key or generate a new one if missing."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    return regenerate_key()

def regenerate_key():
    """Generate and save a new AES-256 key."""
    key = os.urandom(32)
    save_key(key)
    print("🔑 A new AES key has been generated and saved.")
    return key

def encrypt(plain_text, key):
    """Encrypt plaintext with AES-CFB mode."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(plain_text.encode()) + encryptor.finalize()
    return iv + encrypted_data

def decrypt(cipher_text, key):
    """Decrypt AES-CFB ciphertext."""
    if len(cipher_text) < 16:
        raise ValueError("Ciphertext is too short to contain an IV.")
    iv = cipher_text[:16]
    encrypted_data = cipher_text[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(encrypted_data) + decryptor.finalize()).decode()

def menu():
    """Simple CLI Menu for AES Encryption and Decryption."""
    while True:
        print("\nOptions:")
        print("  (E) Encrypt")
        print("  (D) Decrypt")
        print("  (R) Regenerate Key")
        print("  (Q) Quit")
        
        choice = input("\nYour choice: ").strip().lower()

        if choice == "e":
            key = load_key()
            plain_text = input("Enter text to encrypt: ")
            cipher_text = encrypt(plain_text, key)
            print("\n🔒 Encrypted (Hex):", cipher_text.hex())

        elif choice == "d":
            key = load_key()
            cipher_text_hex = input("Enter hex-encoded ciphertext: ").strip()
            try:
                cipher_text = bytes.fromhex(cipher_text_hex)
                decrypted_text = decrypt(cipher_text, key)
                print("\n✅ Decrypted text:", decrypted_text)
            except Exception as e:
                print("❌ Decryption failed:", e)

        elif choice == "r":
            regenerate_key()

        elif choice == "q":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter E, D, R or Q.")

if __name__ == "__main__":
    menu()
