from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QRadioButton, QHBoxLayout
import sys
from rc4_logic import encrypt, decrypt

class RC4App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC4 Chiffrement / Déchiffrement (Base64)")
        self.resize(450, 300)

        layout = QVBoxLayout()

        self.mode_label = QLabel("Choisissez le mode :")
        self.encrypt_radio = QRadioButton("Chiffrement")
        self.decrypt_radio = QRadioButton("Déchiffrement")
        self.encrypt_radio.setChecked(True)

        self.input_label = QLabel("Texte clair ou chiffré (Base64) :")
        self.input_text = QTextEdit()

        self.key_label = QLabel("Clé (texte, nombre ou mixte) :")
        self.key_input = QLineEdit()

        self.process_button = QPushButton("Exécuter")
        self.result_label = QLabel("Résultat :")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addWidget(self.mode_label)
        h_mode = QHBoxLayout()
        h_mode.addWidget(self.encrypt_radio)
        h_mode.addWidget(self.decrypt_radio)
        layout.addLayout(h_mode)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)

        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)

        layout.addWidget(self.process_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

        self.process_button.clicked.connect(self.process)

    def process(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not key:
            self.result_text.setPlainText("❌ La clé ne peut pas être vide !")
            return

        if self.encrypt_radio.isChecked():
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)

        self.result_text.setPlainText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RC4App()
    window.show()
    sys.exit(app.exec_())
