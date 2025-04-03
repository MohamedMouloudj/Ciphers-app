from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QComboBox
import sys

class VigenereCipher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.label_option = QLabel("Choisissez une option:")
        layout.addWidget(self.label_option)

        self.option_box = QComboBox()
        self.option_box.addItems(["Chiffrer", "Déchiffrer", "Trouver la clé"])
        layout.addWidget(self.option_box)

        self.label_text = QLabel("1.Text_clair / 2.Text_chiffré / 3.Text_clair :")
        layout.addWidget(self.label_text)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.label_key = QLabel("1.Clé / 2.clé / 3.Text_chiffré :")
        layout.addWidget(self.label_key)

        self.key_input = QTextEdit()
        layout.addWidget(self.key_input)

        self.run_button = QPushButton("Exécuter")
        self.run_button.clicked.connect(self.process)
        layout.addWidget(self.run_button)

        self.result_label = QLabel("Résultat:")
        layout.addWidget(self.result_label)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)
        self.setWindowTitle("Chiffrement de Vigenère")

    def vigenere_chiffrer(self, texte, cle):
        resultat = ""
        cle = cle.upper()
        index = 0
        for char in texte:
            if char.isalpha():
                shift = ord(cle[index % len(cle)]) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                resultat += chr((ord(char) - base + shift) % 26 + base)
                index += 1
            else:
                resultat += char
        return resultat

    def vigenere_dechiffrer(self, texte, cle):
        resultat = ""
        cle = cle.upper()
        index = 0
        for char in texte:
            if char.isalpha():
                shift = ord(cle[index % len(cle)]) - ord('A')
                base = ord('A') if char.isupper() else ord('a')
                resultat += chr((ord(char) - base - shift) % 26 + base)
                index += 1
            else:
                resultat += char
        return resultat

    def trouver_cle(self, texte, texte_chiffre):
        cle = ""
        for i in range(len(texte)):
            if texte[i].isalpha() and texte_chiffre[i].isalpha():
                base = ord('A') if texte[i].isupper() else ord('a')
                shift = (ord(texte_chiffre[i]) - ord(texte[i])) % 26
                cle += chr(base + shift)
            else:
                cle += " "  # Ajoute un espace pour garder l'alignement
        return cle.strip()

    def process(self):
        option = self.option_box.currentIndex()
        texte = self.text_input.toPlainText().strip()
        cle_ou_texte_chiffre = self.key_input.toPlainText().strip()

        if option == 0:
            result = self.vigenere_chiffrer(texte, cle_ou_texte_chiffre)
        elif option == 1:
            result = self.vigenere_dechiffrer(texte, cle_ou_texte_chiffre)
        elif option == 2:
            result = self.trouver_cle(texte, cle_ou_texte_chiffre)
        
        self.result_output.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereCipher()
    window.show()
    sys.exit(app.exec_())
