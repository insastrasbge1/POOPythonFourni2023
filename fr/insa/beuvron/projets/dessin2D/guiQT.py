# Copyright 2022 Francois de Bertrand de Beuvron
#
# This file is part of CoursBeuvron.
#
# CoursBeuvron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CoursBeuvron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CoursBeuvron.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on 25 juin 2022

@author: Francois de Bertrand de Beuvron
'''

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from fr.insa.beuvron.projets.dessin2D.model import Groupe,Point,Segment


class FrameAvecBordure(qtw.QFrame):
    # une variable de classe pour définir un comportement par défaut
    # si modifiée : modifie la bordure de toutes les FrameAvecBordure
    # ou le paramètre 'bordure' n'est pas explicitement fourni lors
    # de l'__init__
    DEFAULT_BORDURE = False

    # DEFAULT_BORDURE peut être utilisé dans __init__
    def __init__(self,bordure : bool = DEFAULT_BORDURE):
        super().__init__()
        if bordure :
            # une bordure simple; de nombreuses autres options possibles
            self.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Plain)
            self.setLineWidth(3)

class Entete(FrameAvecBordure) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        layout = qtw.QHBoxLayout()
        self.lPx = qtw.QLabel("x : ")
        layout.addWidget(self.lPx)
        self.tfPx = qtw.QLineEdit()
        layout.addWidget(self.tfPx)
        self.lPy = qtw.QLabel("y : ")
        layout.addWidget(self.lPy)
        self.tfPy = qtw.QLineEdit()
        layout.addWidget(self.tfPy)
        self.bCreePoint = qtw.QPushButton("crée Point")
        layout.addWidget(self.bCreePoint)
        self.bCreePoint.clicked.connect(self.doCreation)
        self.bChangeColor = ChooseColorButton()
        layout.addWidget(self.bChangeColor)
        self.setLayout(layout)

    def doCreation(self):
        px = float(self.tfPx.text())
        py = float(self.tfPy.text())
        p = Point(px,py)
        self._main.model.add_figure(p)
        self._main.updateView()

class PanneauGauche(FrameAvecBordure):
    def __init__(self, main: 'Main'):
        super().__init__()
        self._main = main
        layout = qtw.QVBoxLayout()
        self.bPoint = qtw.QRadioButton("Point")
        layout.addWidget(self.bPoint)
        self.bSegment = qtw.QRadioButton("Segment")
        layout.addWidget(self.bSegment)
        self.bSelection = qtw.QRadioButton("Selection")
        layout.addWidget(self.bSelection)
        self.bPoint.toggled.connect(self.changeMode)
        self.bSegment.toggled.connect(self.changeMode)
        self.bSelection.toggled.connect(self.changeMode)
        group = qtw.QButtonGroup()
        group.addButton(self.bPoint)
        group.addButton(self.bSegment)
        group.addButton(self.bSegment)
        self.bPoint.setChecked(True)
        self.changeMode()
        self.setLayout(layout)

    def changeMode(self):
        print("change mode")
        if self.bPoint.isChecked() :
            print(" mode point")
            self._main.controleur.modeCreationPoint()
        elif self.bSegment.isChecked() :
            print(" mode segment")
            self._main.controleur.modeCreationSegment()
        else :
            print(" mode point")
            self._main.controleur.modeSelection()


class ZoneDessinTexte(qtw.QPlainTextEdit) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self.appendPlainText(self._main.model.str_detail())

    def updateView(self):
       self.document().setPlainText(self._main.model.str_detail())

class SceneDessinGraphics(qtw.QGraphicsScene) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self.redessine()

    def redessine(self):
        self.clear()
        model = self._main.model
        for fig in model.contient :
            fig.dessine(self)

    def mousePressEvent(self, event:qtw.QGraphicsSceneMouseEvent):
        self._main.controleur.gereClicSouris(event)

class ZoneDessinGraphics(qtw.QGraphicsView) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self._scene = SceneDessinGraphics(main);
        self.setScene(self._scene)

    def updateView(self):
        self._scene.redessine()

class ChooseColorButton(qtw.QPushButton):
    def __init__(self,color : qtg.QColor = qtg.QColor(0,0,0)):
        super().__init__("change color...")
        self.curColor = color
        self.clicked.connect(self.doChoose)

    def doChoose(self):
        dlg = qtw.QColorDialog(self)
        dlg.setCurrentColor(self.curColor)
        if dlg.exec() :
            self.curColor = dlg.currentColor()
            print("curcolor : " + str(self.curColor))

class Main(FrameAvecBordure) :
    def __init__(self,model : 'Groupe'):
        super().__init__()
        self._model = model
        self._controleur = Controleur(self)
        mainL = qtw.QVBoxLayout()
        self.entete = Entete(self)
        mainL.addWidget(self.entete)
        horLayout = qtw.QHBoxLayout()
        self.left = PanneauGauche(self)
        horLayout.addWidget(self.left)
        #self._zoneDessin = ZoneDessinTexte(self)
        self.zoneDessin = ZoneDessinGraphics(self)
        horLayout.addWidget(self.zoneDessin)
        comp = qtw.QWidget()
        comp.setLayout(horLayout)
        mainL.addWidget(comp)
        self.setLayout(mainL)

    @property
    def model(self):
        return self._model

    @property
    def controleur(self):
        return self._controleur

    def updateView(self):
        self.zoneDessin.updateView()


class Controleur():
    """
    les états sont représentés par des entiers :
    20 : mode sélection
    30 : mode création de points
    40 : mode création de segment, en attente du premier point
    41 : mode création de segment, en attente du second point
    """
    def __init__(self,main : 'Main'):
        self._main = main
        # on commence en mode création de points
        self._state = 30

    def modeSelection(self):
        self._state = 20

    def modeCreationPoint(self):
        self._state = 30

    def modeCreationSegment(self):
        self._state = 40

    def gereClicSouris(self,event:qtw.QGraphicsSceneMouseEvent) -> None:
        px = event.scenePos().x()
        py = event.scenePos().y()
        curColor = self._main.entete.bChangeColor.curColor
        if self._state == 30 :
            self._main.model.add_figure(Point(px, py,curColor))
            self._main.updateView()
        elif self._state == 40 :
            self._premierPoint = Point(px,py)
            self._state = 41
        elif self._state == 41 :
            p2 = Point(px,py)
            seg = Segment(self._premierPoint,p2,curColor)
            self._main.model.add_figure(seg)
            self._main.updateView()
            self._state = 40

def gogogo() :
    app = qtw.QApplication()  # toujours 1 objet de type QApplication
    model = Groupe.groupe_alea(10,5)
    print(model.str_detail())
    main = Main(model)
    #test = Entete(main)
    #test.show()
    main.show()
    app.exec()  # démarre l'application QT.

if __name__ == '__main__':
    gogogo()
