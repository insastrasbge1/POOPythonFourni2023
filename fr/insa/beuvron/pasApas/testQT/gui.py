import PySide6.QtWidgets as qtw
from model import Point
from model import Dessin

class EditPoints(qtw.QWidget) :

    def __init__(self,model : Dessin = None):
        super().__init__()
        if model is None :
            self._model = Dessin()
        else :
            self._model = model
        lpx = qtw.QLabel("px : ")
        lpy = qtw.QLabel("py : ")
        self._tfPx = qtw.QLineEdit()
        self._tfPy = qtw.QLineEdit()
        self._bCree = qtw.QPushButton("Cree Point")
        meth = self.doCreation
        self._bCree.clicked.connect(meth)
        cree_layout = qtw.QHBoxLayout()
        cree_layout.addWidget(lpx)
        cree_layout.addWidget(self._tfPx)
        cree_layout.addWidget(lpy)
        cree_layout.addWidget(self._tfPy)
        cree_layout.addWidget(self._bCree)

        self._affTexte = qtw.QTextEdit()
        self._affTexte.setReadOnly(True)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(cree_layout)
        main_layout.addWidget(self._affTexte)

        self.setLayout(main_layout)

    def doCreation(self):
        px = int(self._tfPx.text())
        py = int(self._tfPy.text())
        p = Point(px,py)
        self._model.ajout(p)
        self._affTexte.setText(str(self._model))

def debut():
    app = qtw.QApplication()
    ep = EditPoints()
    ep.show()
    app.exec()

if __name__ == '__main__':
    debut()
