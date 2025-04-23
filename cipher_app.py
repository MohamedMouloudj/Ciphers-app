import sys
import platform
from PyQt5 import QtWidgets, uic
import cffi
import os

# This is the list of libraries we will use for the ciphers
libraries=[
    "caesar",
    "vigenere",
    "substitution",
    "Analyse_frequentielle",
    "Coincidence_index", 
    "playfair",
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
        elif cipher == "Analyse_frequentielle":
            self.prvInput.setPlaceholderText("Enter a text")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "Coincidence_index":
            self.prvInput.setPlaceholderText("Enter a text")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "vigenere":
            self.prvInput.setPlaceholderText("Enter a keyword")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "substitution":
            self.prvInput.setPlaceholderText("Enter 26 letters (a-z)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "playfair":
            self.prvInput.setPlaceholderText("Enter a keyword")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "RSA":
            self.prvInput.setPlaceholderText("Private key")
            self.pubInput.setPlaceholderText("Public key")
            self.pubInput.setEnabled(True)
        elif cipher == "AES":
            self.prvInput.setPlaceholderText("Enter key (16, 24, or 32 bytes)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
    
    def process_cipher(self):
        """Process the encryption/decryption when Launch button is clicked"""
        cipher = self.cipherCombo.currentText()
        prv_key = self.prvInput.text()
        pub_key = self.pubInput.text()
        encrypt_text = self.encryptInput.toPlainText()
        decrypt_text = self.decryptInput.toPlainText()
        if cipher == "playfair":
            if encrypt_text:
                encrypt_text = ''.join(filter(str.isalpha, encrypt_text)).upper()
                self.encryptInput.setPlainText(encrypt_text)
    
            if decrypt_text:
                decrypt_text = ''.join(filter(str.isalpha, decrypt_text)).upper()
                self.decryptInput.setPlainText(decrypt_text)

        
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