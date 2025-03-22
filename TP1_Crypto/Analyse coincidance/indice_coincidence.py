from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
import sys

def calculer_indice_coincidence(texte):
    frequences = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
    total_lettres = 0
    
    for c in texte.lower():
        if 'a' <= c <= 'z':
            frequences[c] += 1
            total_lettres += 1
    
    if total_lettres <= 1:
        return 0.0
    
    ic = sum(f * (f - 1) for f in frequences.values()) / (total_lettres * (total_lettres - 1))
    return ic

class ICApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Entrez le texte :")
        layout.addWidget(self.label)
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        
        self.button = QPushButton("Calculer l'Indice de Coïncidence")
        self.button.clicked.connect(self.calculate_ic)
        layout.addWidget(self.button)
        
        self.result_label = QLabel("Indice de Coïncidence : N/A")
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
        self.setWindowTitle("Analyse IC")
    
    def calculate_ic(self):
        texte = self.text_edit.toPlainText()
        ic = calculer_indice_coincidence(texte)
        self.result_label.setText(f"Indice de Coïncidence : {ic:.6f}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ICApp()
    ex.show()
    sys.exit(app.exec_())
