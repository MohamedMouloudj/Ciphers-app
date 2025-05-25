import sys
import platform
from PyQt5 import QtWidgets, uic
import cffi
import os
import math
import sys
import re
from modernCiphers import des_encrypt, des_decrypt, rc4_encrypt, rc4_decrypt, aes_encrypt, aes_decrypt, otp_decrypt, otp_encrypt, setCustomKeys, RSA_encrypt, RSA_decrypt, generate_dh_public_key, calculate_shared_secret, dh_encrypt, dh_decrypt, elgamal_encrypt, elgamal_decrypt, power

# This is the list of libraries we will use for the ciphers
libraries=[
    "caesar",
    "vigenere",
    "playfair",
    "affine",
    "hill",
    "substitution",
    "Analyse_frequentielle",
    "Coincidence_index",
    "One-Time Pad",
    "DES",
    "AES (128)",
    "RC4",
    "RSA (2048)",
    "ElGamal",
    "Diffie-Hellman",
    "MD5",
    "SHA-256",
]

def get_shared_library(lib_name):
    """Get the absolute path of the shared library based on the OS"""
    system_name = platform.system()
    if system_name not in ["Windows", "Linux"]:
        raise Exception("Unsupported OS")
    ext = {"Windows": ".dll", "Linux": ".so"}[system_name]
    return os.path.abspath(f"./{lib_name}{ext}")

class CipherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi('ciphers-list.ui', self)
        self.ffi = cffi.FFI()
        
        self.setWindowTitle("Ciphers Application")
        self.cipherCombo = self.findChild(QtWidgets.QComboBox, 'cipherCombo')
        self.prvInput = self.findChild(QtWidgets.QLineEdit, 'prvInput')
        self.pubInput = self.findChild(QtWidgets.QLineEdit, 'pubInput')
        self.encryptInput = self.findChild(QtWidgets.QPlainTextEdit, 'encryptInput')
        self.decryptInput = self.findChild(QtWidgets.QPlainTextEdit, 'decryptInput')
        self.launch = self.findChild(QtWidgets.QPushButton, 'launch')
        
        # Cipher options, we will add more, this is a placeholder
        self.cipherCombo.addItems(libraries)
        
        # connect signals (events) to slots (functions)
        self.cipherCombo.currentIndexChanged.connect(self.cipher_changed)
        self.launch.clicked.connect(self.process_cipher)
        
        # Load main.c library for cipher functions
        try:
            lib_name = "classical-ciphers/main"
            self.ffi.cdef("""
                const char* handle_cipher_file(const char* filename);
            """)
            self.cipher_lib = self.ffi.dlopen(get_shared_library(lib_name))
        except Exception as e:
            print(f"Error loading C library: {e}")
            self.cipher_lib = None

        self.cipher_changed(0)
        
    def cipher_changed(self, index):
        """Update key input fields based on selected cipher"""
        cipher = self.cipherCombo.currentText()
        
        # Adjust UI based on cipher selection
        if cipher == "caesar":
            self.prvInput.setPlaceholderText("Enter a number (1-25)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "Analyse_frequentielle":
            self.prvInput.setPlaceholderText("")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(False)
            self.decryptInput.setEnabled(False)
            self.encryptInput.setPlaceholderText("Enter a text to analyze")
        elif cipher == "Coincidence_index":
            self.prvInput.setPlaceholderText("")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(False)
            self.decryptInput.setEnabled(False)
            self.encryptInput.setPlaceholderText("Enter a text to analyze")
        elif cipher == "vigenere":
            self.prvInput.setPlaceholderText("Enter a keyword")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "substitution":
            self.prvInput.setPlaceholderText("Enter 26 letters (a-z)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "playfair":
            self.prvInput.setPlaceholderText("Enter a keyword")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "affine":
            self.prvInput.setPlaceholderText("Enter a,b (comma separated)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "hill":
            self.prvInput.setPlaceholderText("Enter key (comma-separated integers 0-25)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)

            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
            self.encryptInput.setPlaceholderText("Enter text to encrypt")
        elif cipher == "RSA (2048)":
            self.prvInput.setPlaceholderText("Private key (PEM format)")
            self.pubInput.setPlaceholderText("Public key (PEM format)")
            self.pubInput.setEnabled(True)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "ElGamal":
            self.prvInput.setPlaceholderText("Private key")
            self.pubInput.setPlaceholderText("Public key")
            self.pubInput.setEnabled(True)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "Diffie-Hellman":
            self.prvInput.setPlaceholderText("Private key")
            self.pubInput.setPlaceholderText("Public key")
            self.pubInput.setEnabled(True)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "AES (128)":
            self.prvInput.setPlaceholderText("Enter key (16 bytes)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "DES":
            self.prvInput.setPlaceholderText("Enter key (8 bytes)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "RC4":
            self.prvInput.setPlaceholderText("Enter key (any length)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)
        elif cipher == "One-Time Pad":
            self.prvInput.setPlaceholderText("Enter key (same length as text)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
            self.prvInput.setEnabled(True)
            self.decryptInput.setEnabled(True)

    def process_cipher(self):
        """Process the encryption/decryption when Launch button is clicked"""
        cipher = self.cipherCombo.currentText()
        prv_key = self.prvInput.text() if self.prvInput.text() else ''
        pub_key = self.pubInput.text()
        encrypt_text = self.encryptInput.toPlainText()
        decrypt_text = self.decryptInput.toPlainText()
        needs_C_call=False
        # Validate keys based on cipher
        if cipher == "playfair" or cipher == "substitution":
            needs_C_call = True
            if encrypt_text:
                encrypt_text = ''.join(filter(str.isalpha, encrypt_text)).upper()
                self.encryptInput.setPlainText(encrypt_text)
    
            if decrypt_text:
                decrypt_text = ''.join(filter(str.isalpha, decrypt_text)).upper()
                self.decryptInput.setPlainText(decrypt_text)
        elif cipher == "caesar":
            needs_C_call = True
            if encrypt_text:
                try:
                    shift = int(prv_key)
                    if not (1 <= shift <= 25):
                        raise ValueError("Shift must be between 1 and 25")
                    encrypt_text = ''.join(filter(str.isalpha, encrypt_text)).upper()
                    self.encryptInput.setPlainText(encrypt_text)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
                    return
    
            if decrypt_text:
                try:
                    shift = int(prv_key)
                    if not (1 <= shift <= 25):
                        raise ValueError("Shift must be between 1 and 25")
                    decrypt_text = ''.join(filter(str.isalpha, decrypt_text)).upper()
                    self.decryptInput.setPlainText(decrypt_text)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
                    return
        elif cipher == "vigenere":
            needs_C_call = True
            if encrypt_text:
                encrypt_text = ''.join(filter(str.isalpha, encrypt_text)).upper()
                self.encryptInput.setPlainText(encrypt_text)
    
            if decrypt_text:
                decrypt_text = ''.join(filter(str.isalpha, decrypt_text)).upper()
                self.decryptInput.setPlainText(decrypt_text)
        elif cipher == "Analyse_frequentielle" or cipher == "Coincidence_index":
            needs_C_call = True
            if encrypt_text:
                encrypt_text = ''.join(filter(str.isalpha, encrypt_text))
                self.encryptInput.setPlainText(encrypt_text)
            if decrypt_text:
                decrypt_text = ''.join(filter(str.isalpha, decrypt_text))
                self.decryptInput.setPlainText(decrypt_text)
        elif cipher == "affine":
            needs_C_call = True
            if encrypt_text:
                try:
                    a, b = map(int, prv_key.split(','))
                    if a <= 0 or b < 0:
                        raise ValueError("Invalid affine key")
                    if (not math.gcd(a, 26) == 1):
                        raise ValueError("a must be coprime with 26")
                    encrypt_text = ''.join(filter(str.isalpha, encrypt_text))
                    self.encryptInput.setPlainText(encrypt_text)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
                    return
    
            if decrypt_text:
                try:
                    a, b = map(int, prv_key.split(','))
                    if a <= 0 or b < 0:
                        raise ValueError("Invalid affine key")
                    if (not math.gcd(a, 26) == 1):
                        raise ValueError("a must be coprime with 26")
                    decrypt_text = ''.join(filter(str.isalpha, decrypt_text))
                    self.decryptInput.setPlainText(decrypt_text)
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
                    return
        elif cipher == "hill":
            needs_C_call = True
            # Validating the Hill cipher key format
            if encrypt_text or decrypt_text:
                try:
                    # Parse the key as a comma-separated list of integers
                    if not prv_key:
                        raise ValueError("Key is required for Hill cipher")
                        
                    key_values = [int(k) for k in prv_key.split(',')]
                    
                    # Check if we have a perfect square number of values
                    key_size = len(key_values)
                    matrix_dim = int(math.sqrt(key_size))
                    
                    if matrix_dim * matrix_dim != key_size:
                        raise ValueError(f"Key must form a square matrix. Got {key_size} values.")
                        
                    # Check if all values are between 0-25
                    if any(k < 0 or k > 25 for k in key_values):
                        raise ValueError("All matrix values must be between 0 and 25")
                    
                    # For Hill cipher, we need to make sure the matrix is invertible in modulo 26
                    # The C implementation will handle the actual matrix operations
                    
                except ValueError as e:
                    QtWidgets.QMessageBox.warning(self, "Input Error", str(e))
                    return
                
            if encrypt_text:
                encrypt_text = ''.join(filter(str.isalpha, encrypt_text)).upper()
                self.encryptInput.setPlainText(encrypt_text)
    
            if decrypt_text:
                decrypt_text = ''.join(filter(str.isalpha, decrypt_text)).upper()
                self.decryptInput.setPlainText(decrypt_text)
        elif cipher == "DES":
            if len(prv_key) != 16 or not re.fullmatch(r'[0-9A-Fa-f]{16}', prv_key):
                QtWidgets.QMessageBox.warning(self, "Input Error", "DES key must be exactly 16 hex characters (64 bits)")
                return
    
            try:
                if encrypt_text:
                    # Encrypt text input
                    ciphertext = des_encrypt(encrypt_text, prv_key.upper())
                    self.decryptInput.setPlainText(ciphertext)
        
                if decrypt_text:
                    # Validate hex input for decryption
                    if not re.fullmatch(r'[0-9A-Fa-f]*', decrypt_text) or len(decrypt_text) % 16 != 0:
                        QtWidgets.QMessageBox.warning(self, "Input Error", "DES decrypt input must be valid hex string with length multiple of 16")
                        return
                
                    print(f"Decrypting: {decrypt_text}")
                    decrypted_text = des_decrypt(decrypt_text.upper(), prv_key.upper())
                    self.encryptInput.setPlainText(decrypted_text)
            
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "DES Error", f"DES operation failed: {str(e)}")
                print(f"DES Error: {e}")
        elif cipher == "RC4":
            if len(prv_key) < 1:
                QtWidgets.QMessageBox.warning(self, "Input Error", "RC4 key must be at least 1 character long")
                return
            if encrypt_text:
                result_enc= rc4_encrypt(encrypt_text, prv_key)
                self.decryptInput.setPlainText(result_enc)
            if decrypt_text:
                result_dec = rc4_decrypt(decrypt_text, prv_key)
                self.encryptInput.setPlainText(result_dec)
        elif cipher == "AES (128)":
            if len(prv_key) != 16:
                QtWidgets.QMessageBox.warning(self, "Input Error", "AES key must be exactly 16 characters (128 bits)")
                return
            if encrypt_text:
                result_enc = aes_encrypt(encrypt_text, prv_key)
                self.decryptInput.setPlainText(result_enc)
            if decrypt_text:
                result_dec = aes_decrypt(decrypt_text, prv_key)
                self.encryptInput.setPlainText(result_dec)
        elif cipher == "One-Time Pad":
            if len(prv_key) != len(encrypt_text) and len(prv_key) != len(decrypt_text):
                QtWidgets.QMessageBox.warning(self, "Input Error", "One-Time Pad key must be the same length as the text")
                return
            if encrypt_text:
                result_enc = otp_encrypt(encrypt_text.upper(), prv_key.upper())
                self.decryptInput.setPlainText(result_enc)
            if decrypt_text:
                result_dec = otp_decrypt(decrypt_text, prv_key.upper())
                self.encryptInput.setPlainText(result_dec)
        elif cipher == "RSA (2048)":
        # Parse RSA keys from prv_key (expect format: "p,q" or "p,q,d")
            try:
                e =int(self.pubInput.text() if self.pubInput.text() else '65537')  # Default public exponent
                key_parts = [int(x.strip()) for x in prv_key.split(',')]
                if len(key_parts) == 2:
                    p, q = key_parts
                    d = None
                elif len(key_parts) == 3:
                    p, q, d = key_parts
                else:
                    QtWidgets.QMessageBox.warning(self, "Input Error", "RSA key format: p,q + e or p,q,d + e (comma-separated integers). Note: e is optional, default is 65537")
                    return
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", "RSA keys must be integers separated by commas")
                return
            
            # Validate and set keys
            success, msg, _ = setCustomKeys(p, q, e, d)
            if not success:
                QtWidgets.QMessageBox.warning(self, "Key Error", f"Invalid RSA keys: {msg}")
                return
            # Encrypt/Decrypt
            try:
                if encrypt_text:
                    result_enc, _ = RSA_encrypt(encrypt_text)
                    self.decryptInput.setPlainText(str(result_enc))  # Show as list of numbers
                if decrypt_text:
                    # Parse encrypted data as list of numbers
                    encrypted_data = eval(decrypt_text)  # or use ast.literal_eval for safety
                    result_dec = RSA_decrypt(encrypted_data)
                    self.encryptInput.setPlainText(result_dec)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Encryption Error", str(e))
        elif cipher == "Diffie-Hellman":
            # Parse Diffie-Hellman parameters
            # Expecting: prv_key = private_key, pub_key = "P,G" format or other_party_public_key
            try:
                private_key = int(prv_key)
                if private_key <= 0:
                    raise ValueError("Private key must be a positive integer")
                
                # Check if pub_key contains P,G parameters or is another party's public key
                if ',' in pub_key:
                    # Format: "P,G" - public parameters
                    p_str, g_str = pub_key.split(',', 1)
                    P = int(p_str.strip())
                    G = int(g_str.strip())
                    if P <= 0 or G <= 0:
                        raise ValueError("Both P and G must be positive integers")
                    
                    # Generate our public key
                    our_public_key = generate_dh_public_key(private_key, P, G)
                    self.pubInput.setText(str(our_public_key))
                    
                    # For demo purposes, use our own public key as "other party"
                    # In real use, you'd get this from the other party
                    other_party_public = our_public_key
                else:
                    # Assume pub_key is the other party's public key
                    # Use default P and G values
                    P, G = 23, 9
                    other_party_public = int(pub_key)
                    our_public_key = generate_dh_public_key(private_key, P, G)
                    
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Input Error", f"Invalid Diffie-Hellman parameters: {str(e)}")
                return
            # Calculate shared secret
            try:
                shared_secret = calculate_shared_secret(other_party_public, private_key, P)
                
                # Encrypt/Decrypt
                if encrypt_text and not decrypt_text:
                    result_enc = dh_encrypt(encrypt_text, shared_secret)
                    self.decryptInput.setPlainText(result_enc)
                
                if decrypt_text:
                    result_dec = dh_decrypt(decrypt_text, shared_secret)
                    self.encryptInput.setPlainText("")
                    self.encryptInput.setPlainText(result_dec)
                    
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Encryption/Decryption Error", str(e))
                return
        elif cipher == "ElGamal":
            # Parse ElGamal parameters
            # Expected format: prv_key = private_key, pub_key = "p,g,h" or just use defaults
            try:
                private_key = int(prv_key)
                if private_key <= 0:
                    raise ValueError("Private key must be a positive integer")
                
                # Parse public key parameters
                if pub_key and ',' in pub_key:
                    # Format: "p,g,h" - public key components
                    parts = [x.strip() for x in pub_key.split(',')]
                    if len(parts) >= 3:
                        p = int(parts[0])
                        g = int(parts[1]) 
                        h = int(parts[2])
                    elif len(parts) == 2:
                        # Format: "p,g" - generate h from private key
                        p = int(parts[0])
                        g = int(parts[1])
                        h = power(g, private_key, p)
                    else:
                        raise ValueError("Invalid public key format")
                else:
                    # Use default parameters and generate public key
                    p = 2357  # Default prime
                    g = 2     # Default generator
                    h = power(g, private_key, p)
                
                # Display generated public key components
                self.pubInput.setText(f"{p},{g},{h}")
                
                public_key_tuple = (p, g, h)
                
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Input Error", f"Invalid ElGamal parameters: {str(e)}")
                return
            
            # Encrypt/Decrypt
            try:
                if encrypt_text:
                    ciphertext, c1 = elgamal_encrypt(encrypt_text, public_key_tuple)
                    # Format output as "c1:[ciphertext_list]"
                    result_enc = f"{c1}:{','.join(map(str, ciphertext))}"
                    self.decryptInput.setPlainText(result_enc)
                
                if decrypt_text:
                    # Parse decrypt input format "c1:ciphertext_list"
                    if ':' in decrypt_text:
                        c1_str, cipher_str = decrypt_text.split(':', 1)
                        c1 = int(c1_str)
                        ciphertext = [int(x) for x in cipher_str.split(',')]
                        result_dec = elgamal_decrypt(ciphertext, c1, private_key, p)
                        self.encryptInput.setPlainText(result_dec)
                    else:
                        raise ValueError("Invalid ciphertext format. Expected 'c1:cipher1,cipher2,...'")
                    
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Encryption/Decryption Error", str(e))
                return

        # Start processing based on input
        if needs_C_call == True:
            if encrypt_text and not decrypt_text:
                # Encryption mode
                result = self.call_c_cipher(encrypt_text, prv_key, pub_key, cipher, encrypt=True)
                self.decryptInput.setPlainText(result)
            elif decrypt_text and not encrypt_text:
                # Decryption mode
                result = self.call_c_cipher(decrypt_text, prv_key, pub_key, cipher, encrypt=False)
                self.encryptInput.setPlainText(result)
            elif encrypt_text and decrypt_text:
                # Both inputs have text (mistake), prioritize encryption
                result = self.call_c_cipher(encrypt_text, prv_key, pub_key, cipher, encrypt=True)
                self.decryptInput.setPlainText(result)
            else:
                # No input text
                QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter text to encrypt or decrypt")
    
    def call_c_cipher(self, text, prv_key, pub_key, cipher, encrypt=True):
        """Call the C library to handle the cipher operation"""	
        
        if self.cipher_lib is None:
            QtWidgets.QMessageBox.critical(self, "Library Error", "C library not loaded")
            return
        if encrypt:
            mode = "encrypt"
        else:
            mode = "decrypt"
        with open("cipher_input.txt", "w") as f:
            f.write(f"cipher: {cipher}\n")
            f.write(f"mode: {mode}\n")
            f.write(f"plain_text: {text}\n")
            f.write(f"prv_key: {prv_key}\n")
            f.write(f"pub_key: {pub_key}\n")

        result_ptr = self.cipher_lib.handle_cipher_file(b"cipher_input.txt")
        if result_ptr == self.ffi.NULL:
            print("C function returned NULL!")
            return "Error: NULL pointer from C"

        try:
            result = self.ffi.string(result_ptr).decode("utf-8")
        except Exception as e:
            print(f"Failed to decode result: {e}")
            return "Error decoding result"

        os.remove("cipher_input.txt")
        return result
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())
