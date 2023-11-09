import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
from model import Point
from model import Dessin

class EditPoints(qtw.QFrame) :

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

        self._zoneDessin = DessinView(self)

        split = qtw.QSplitter(qtc.Qt.Orientation.Vertical)
        split.addWidget(self._zoneDessin)
        split.addWidget(self._affTexte)

        main_layout = qtw.QVBoxLayout()
        main_layout.addLayout(cree_layout)
        main_layout.addWidget(split)

        self.setLayout(main_layout)
        self.updateView()

    @property
    def model(self) -> Dessin:
        return self._model

    def doCreation(self):
        px = int(self._tfPx.text())
        py = int(self._tfPy.text())
        p = Point(px,py)
        self._model.ajout(p)
        self.updateView()

    def updateView(self):
        self._affTexte.setText(str(self._model))
        self._zoneDessin.updateView()


class DessinScene(qtw.QGraphicsScene):
    def __init__(self,main : EditPoints):
        super().__init__()
        self._main = main
        self.updateView()

    def updateView(self):
        m = self._main.model
        self.clear()
        for p in m.contient :
            rep = qtw.QGraphicsEllipseItem(p.px - 5,
                                           p.py - 5,
                                           10,10)
            pen = qtg.QPen(qtg.QPen(qtg.QColor(255,0,0), 2))
            rep.setPen(pen)
            self.addItem(rep)

    def mousePressEvent(self, event: qtw.QGraphicsSceneMouseEvent) -> None:
        x = event.scenePos().x()
        y = event.scenePos().y()
        print(f"posClic = ({x},{y})")
        nouveau = Point(x,y)
        self._main.model.ajout(nouveau)
        self._main.updateView()

class DessinView(qtw.QGraphicsView) :
    def __init__(self,main : EditPoints):
        super().__init__()
        self._main = main
        self._scene = DessinScene(main)
        self._scene.setSceneRect(0,0,self.width(),self.height())
        self.setScene(self._scene)
        self.updateView()

    def updateView(self):
        self._scene.updateView()



def debut():
    app = qtw.QApplication()
    ep = EditPoints(Dessin.test1())
    ep.show()
    app.exec()

if __name__ == '__main__':
    debut()
