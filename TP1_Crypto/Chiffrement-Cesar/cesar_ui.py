import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QMessageBox

class CesarCipherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chiffrement de César")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label_mode = QLabel("Choisissez une option:")
        layout.addWidget(self.label_mode)
        
        self.radio_encrypt = QRadioButton("Chiffrer")
        self.radio_decrypt = QRadioButton("Déchiffrer")
        self.radio_encrypt.setChecked(True)
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.radio_encrypt)
        mode_layout.addWidget(self.radio_decrypt)
        layout.addLayout(mode_layout)

        self.label_text = QLabel("Entrez le texte:")
        layout.addWidget(self.label_text)
        
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)
        
        self.label_key = QLabel("Entrez la clé (nombre):")
        layout.addWidget(self.label_key)
        
        self.key_input = QLineEdit()
        layout.addWidget(self.key_input)
        
        self.button_submit = QPushButton("Exécuter")
        self.button_submit.clicked.connect(self.run_c_program)
        layout.addWidget(self.button_submit)
        
        self.result_label = QLabel("Résultat: ")
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)

    def run_c_program(self):
        text = self.text_input.text()
        key = self.key_input.text()
        
        if not key.isdigit():
            QMessageBox.warning(self, "Erreur", "La clé doit être un nombre entier.")
            return
        
        mode = "1" if self.radio_encrypt.isChecked() else "2"
        
        try:
            process = subprocess.run(
                ["cesar.exe"],
                input=f"{mode}\n{text}\n{key}\n",
                text=True,
                capture_output=True,
                timeout=5
            )
            
            
            
            output = process.stdout.strip().split("\n")
            result_line = output[-1] if output else "Erreur dans l'exécution"
            self.result_label.setText(f"Résultat: {result_line}")

        except subprocess.TimeoutExpired:
            QMessageBox.critical(self, "Erreur", "Le programme a pris trop de temps à répondre.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CesarCipherUI()
    window.show()
    sys.exit(app.exec_())
