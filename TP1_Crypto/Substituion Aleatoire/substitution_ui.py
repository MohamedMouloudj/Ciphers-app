import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit, QLabel

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class SubstitutionCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chiffrement par Substitution")
        self.setGeometry(100, 100, 900, 400)

        self.layout = QVBoxLayout()
        
        # Table de substitution (1ère ligne : alphabet, 2ème ligne : saisie)
        self.table = QTableWidget(2, 26)
        self.table.setVerticalHeaderLabels(["Alphabet", "Substitution"])
        self.table.setFixedHeight(100)

        # Écrire chaque lettre de l'alphabet sur une seule case
        for i, letter in enumerate(ALPHABET):
            alphabet_item = QTableWidgetItem(letter)
            alphabet_item.setFlags(alphabet_item.flags() & ~2)  # Désactiver l'édition
            self.table.setItem(0, i, alphabet_item)

        # Ajouter la table au layout
        self.layout.addWidget(self.table)

        # Bouton de remplissage aléatoire
        self.random_button = QPushButton("Remplissage Aléatoire")
        self.random_button.clicked.connect(self.fill_random_table)
        self.layout.addWidget(self.random_button)

        # Zone de texte pour entrer le message
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Entrez le texte ici...")
        self.layout.addWidget(self.text_input)

        # Boutons de chiffrement et déchiffrement
        self.encrypt_button = QPushButton("Chiffrer")
        self.decrypt_button = QPushButton("Déchiffrer")
        self.layout.addWidget(self.encrypt_button)
        self.layout.addWidget(self.decrypt_button)

        # Zone de texte pour afficher le résultat
        self.result_label = QLabel("Résultat : ")
        self.layout.addWidget(self.result_label)

        # Connecter les boutons aux fonctions
        self.encrypt_button.clicked.connect(self.chiffrer)
        self.decrypt_button.clicked.connect(self.dechiffrer)

        self.setLayout(self.layout)

    def fill_random_table(self):
        """ Génère une table de substitution aléatoire """
        shuffled_alphabet = list(ALPHABET)
        random.shuffle(shuffled_alphabet)  # Mélanger les lettres
        for i, letter in enumerate(shuffled_alphabet):
            self.table.setItem(1, i, QTableWidgetItem(letter))

    def get_substitution_table(self):
        """ Récupère la table de substitution saisie par l'utilisateur """
        table_substituee = ""
        for i in range(26):
            item = self.table.item(1, i)
            if item and item.text():
                table_substituee += item.text().upper()
            else:
                table_substituee += " "  # Met un espace si vide
        return table_substituee

    def chiffrer(self):
        table_substituee = self.get_substitution_table()
        texte = self.text_input.toPlainText().upper()
        result = ""

        for lettre in texte:
            if lettre in ALPHABET:
                index = ALPHABET.index(lettre)
                result += table_substituee[index]
            else:
                result += lettre  # Garder les caractères non alphabétiques
        
        self.result_label.setText(f"Résultat : {result}")

    def dechiffrer(self):
        table_substituee = self.get_substitution_table()
        texte = self.text_input.toPlainText().upper()
        result = ""

        for lettre in texte:
            if lettre in table_substituee:
                index = table_substituee.index(lettre)
                result += ALPHABET[index]
            else:
                result += lettre  # Garder les caractères non alphabétiques
        
        self.result_label.setText(f"Résultat : {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubstitutionCipherApp()
    window.show()
    sys.exit(app.exec())
