import sys
import platform
from PyQt5 import QtWidgets, uic
import cffi
import os

# This is the list of libraries we will use for the ciphers
libraries={
    "cesar": "classical-cihers/cesar",
    "vigenere":"classical-cihers/vigenere",
    "substitution": "classical-cihers/substitution",
    "Analyse_frequentielle":"classical-cihers/Analyse_frequentielle",
    "Coincidence_index":"classical-cihers/indice_coincidence",
}

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
        self.cipherCombo.addItems(libraries.keys())
        
        # connect signals (events) to slots (functions)
        self.cipherCombo.currentIndexChanged.connect(self.cipher_changed)
        self.launch.clicked.connect(self.process_cipher)
        
        # Load C library for cipher functions
        try:
            lib_name = libraries[self.cipherCombo.currentText()]
            self.cipher_lib = self.ffi.dlopen(get_shared_library(lib_name))
        except Exception as e:
            print(f"Error loading C library: {e}")
            self.cipher_lib = None
        
        # initial cipher
        self.cipher_changed(0)
        
    def cipher_changed(self, index):
        """Update key input fields based on selected cipher"""
        cipher = self.cipherCombo.currentText()
        
        # Adjust UI based on cipher selection
        if cipher == "cesar":
            self.prvInput.setPlaceholderText("Enter a number (1-25)")
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
        
        if encrypt_text and not decrypt_text:
            # Encryption mode
            result = self.call_c_cipher(encrypt_text, prv_key, pub_key, cipher, encrypt=True)
            print(result)
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
    
    def call_c_cipher(self, text, prv_key, pub_key, cipher_type, encrypt=True):
        """Interface with C cipher implementations based on selected cipher type"""
        
        if self.cipher_lib is None:
            QtWidgets.QMessageBox.critical(self, "Library Error", "C library not loaded")
            return
        
        text_bytes = text.encode('utf-8')

        if cipher_type == "cesar":
            self.ffi.cdef("""
                char* chiffrementCesar(char *message, int decalage);
                char* dechiffrementCesar(char *message, int decalage);
            """)

            if encrypt:
                result=self.cipher_lib.chiffrementCesar(text_bytes, int(prv_key)) 
                if result == self.ffi.NULL:
                    raise Exception("Error in encryption")
                result_str=self.ffi.string(result)
                return result_str.decode('utf-8')
            else:
                result=self.cipher_lib.dechiffrementCesar(text_bytes, int(prv_key)) 
                if result == self.ffi.NULL:
                    raise Exception("Error in decryption")
                result_str=self.ffi.string(result)
                return result_str.decode('utf-8')
        elif cipher_type == "vigenere":
            pass
             //added by brahim 
        elif cipher_type == "substitution":
        self.ffi.cdef("""
            char* chiffrementSubstitution(char *message, char *key);
            char* dechiffrementSubstitution(char *message, char *key);
        """)
        
        if encrypt:
            result = self.cipher_lib.chiffrementSubstitution(text_bytes, prv_key.encode('utf-8')) 
            if result == self.ffi.NULL:
                raise Exception("Error in encryption")
            result_str = self.ffi.string(result)
            return result_str.decode('utf-8')
        else:
            result = self.cipher_lib.dechiffrementSubstitution(text_bytes, prv_key.encode('utf-8')) 
            if result == self.ffi.NULL:
                raise Exception("Error in decryption")
            result_str = self.ffi.string(result)
            return result_str.decode('utf-8')
              
            //fin d'ajout by brahim

        # Return placeholder for now
        direction = "encrypted" if encrypt else "decrypted"
        return f"[{direction} with {cipher_type}]: {text}"
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())
