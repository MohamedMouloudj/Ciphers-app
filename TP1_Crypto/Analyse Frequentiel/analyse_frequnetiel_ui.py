from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit
import sys

class AnalyseFrequentielleUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.analyse_button = QPushButton("Analyser la fréquence")
        self.analyse_button.clicked.connect(self.analyser_texte)
        layout.addWidget(self.analyse_button)

        self.result_table = QTableWidget(26, 3)
        self.result_table.setHorizontalHeaderLabels(["Lettre", "Fréquence", "Pourcentage"])
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def analyser_texte(self):
        texte = self.text_input.toPlainText().lower()
        frequences = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
        total_lettres = 0

        for char in texte:
            if char in frequences:
                frequences[char] += 1
                total_lettres += 1

        for i, (lettre, freq) in enumerate(frequences.items()):
            pourcentage = (freq / total_lettres) * 100 if total_lettres > 0 else 0
            self.result_table.setItem(i, 0, QTableWidgetItem(lettre.upper()))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(freq)))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{pourcentage:.2f}%"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnalyseFrequentielleUI()
    window.show()
    sys.exit(app.exec_())
