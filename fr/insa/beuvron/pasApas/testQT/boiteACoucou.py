
import PySide6.QtWidgets as qtw

class BoiteACoucou(qtw.QWidget) :

    def __init__(self):
        super().__init__()
        main_layout = qtw.QVBoxLayout()
        lNom = qtw.QLabel("nom :")
        self._tfNom = qtw.QLineEdit()
        entete_layout = qtw.QHBoxLayout()
        entete_layout.addWidget(lNom)
        entete_layout.addWidget(self._tfNom)
        main_layout.addLayout(entete_layout)
        self._taMessage = qtw.QTextEdit()
        self._taMessage.setReadOnly(True)
        main_layout.addWidget(self._taMessage)
        self._bCoucou = qtw.QPushButton("Coucou")
        self._bCoucou.clicked.connect(self.doCoucou)
        self._bSalut = qtw.QPushButton("Salut")
        self._bSalut.clicked.connect(self.doSalut)
        self._boutons_layout = qtw.QHBoxLayout()
        self._boutons_layout.addWidget(self._bCoucou)
        self._boutons_layout.addWidget(self._bSalut)
        main_layout.addLayout(self._boutons_layout)

        self.setLayout(main_layout)

    def doCoucou(self):
        nom = self._tfNom.text()
        self._taMessage.append("coucou " + nom)

    def doSalut(self):
        nom = self._tfNom.text()
        self._bAjoute = qtw.QPushButton("Ajout")
        self._bAjoute.clicked.connect(self.doAjout)
        self._boutons_layout.addWidget(self._bAjoute)
        self._taMessage.append("salut " + nom)

    def doAjout(self):
        self._taMessage.append("je ne sais pas ajouter ")

def debut():
    app = qtw.QApplication()
    bac = BoiteACoucou()
    bac.show()
    app.exec()

if __name__ == '__main__':
    debut()
