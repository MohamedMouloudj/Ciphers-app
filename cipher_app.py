import sys
import os
from PyQt5 import QtWidgets, uic
import ctypes

class CipherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        uic.loadUi('ciphers-list.ui', self)
        
        self.setWindowTitle("Ciphers Application")
        
        self.cipherCombo = self.findChild(QtWidgets.QComboBox, 'cipherCombo')
        self.prvInput = self.findChild(QtWidgets.QLineEdit, 'prvInput')
        self.pubInput = self.findChild(QtWidgets.QLineEdit, 'pubInput')
        self.encryptInput = self.findChild(QtWidgets.QPlainTextEdit, 'encryptInput')
        self.decryptInput = self.findChild(QtWidgets.QPlainTextEdit, 'decryptInput')
        self.launch = self.findChild(QtWidgets.QPushButton, 'launch')
        
        # Cipher options, we will add more, this is a placeholder
        self.cipherCombo.addItems(["Caesar", "Vigenere", "Substitution", "RSA", "AES"])
        
        # connect signals (events) to slots (functions)
        self.cipherCombo.currentIndexChanged.connect(self.cipher_changed)
        self.launch.clicked.connect(self.process_cipher)
        
        # Load C library for cipher functions
        try:
            # Adjust the path to where your C library is located
            # self.cipher_lib = ctypes.CDLL("./ciphers.so")
            self.cipher_lib = None  # Comment this and uncomment above line when you have the library
        except Exception as e:
            print(f"Error loading C library: {e}")
            self.cipher_lib = None
        
        # initial cipher
        self.cipher_changed(0)
        
    def cipher_changed(self, index):
        """Update key input fields based on selected cipher"""
        cipher = self.cipherCombo.currentText()
        
        # Adjust UI based on cipher selection
        if cipher == "Caesar":
            self.prvInput.setPlaceholderText("Enter a number (1-25)")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "Vigenere":
            self.prvInput.setPlaceholderText("Enter a keyword")
            self.pubInput.setPlaceholderText("")
            self.pubInput.setEnabled(False)
        elif cipher == "Substitution":
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
        """Interface with C cipher implementations"""
        if self.cipher_lib is None:
            # Placeholder implementation when C library is not available
            direction = "encrypted" if encrypt else "decrypted"
            return f"[{direction} with {cipher_type}]: {text}"
        
        # This is where we would call our C functions through ctypes
        # ex:
        '''
        if cipher_type == "Caesar":
            if encrypt:
                # Create buffer for result
                result_buffer = ctypes.create_string_buffer(len(text) * 2)
                # Call C function
                self.cipher_lib.caesar_encrypt(
                    text.encode('utf-8'),           # Input text
                    ctypes.c_int(int(prv_key)),     # Key as integer
                    result_buffer,                  # Buffer for result
                    ctypes.c_int(len(result_buffer))# Buffer size
                )
                return result_buffer.value.decode('utf-8')
            else:
                # Similar for decryption
                # ...
        '''
        # Return placeholder for now
        direction = "encrypted" if encrypt else "decrypted"
        return f"[{direction} with {cipher_type}]: {text}"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())