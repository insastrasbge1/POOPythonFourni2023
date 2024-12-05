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
"""
définition très simplifiée d'un circuit avec noeuds et composants.
Ne contient que ce qui est utile pour tester le calcul des mailles

@author: Francois de Bertrand de Beuvron
"""

import math
import abc
from typing import Optional
import syslinZMod2

class Noeud:

    def __init__(self, nom: str):
        self._nom = nom

    @property
    def nom(self) -> str:
        return self._nom


    def __str__(self):
        return self.nom

class Composant():
    def __init__(self,nom : str, depart: 'Noeud', arrivee: 'Noeud'):
        self._nom = nom
        self._depart = depart
        self._arrivee = arrivee

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def depart(self) -> 'Noeud':
        return self._depart

    @property
    def arrivee(self) -> 'Noeud':
        return self._arrivee

    def noeudOppose(self,n : 'Noeud') -> 'Noeud':
        if n == self.depart :
            return self.arrivee
        elif n == self.arrivee :
            return self.depart
        else :
            raise Exception("noeud n'est pas sur le composant")

    def __str__(self):
        return f"-{self.nom}->"


class Circuit:
    def __init__(self,noeuds : list[Noeud] = None,composants : list[Composant] = None):
        if noeuds == None :
            self._noeuds = []
        else :
            self._noeuds = noeuds
        if composants == None :
            self._composants = []
        else :
            self._composants = composants

    @property
    def noeuds(self) -> list['Noeud']:
        return self._noeuds

    @property
    def composants(self) -> list['Composant']:
        return self._composants

    def __str__(self):
        res = "Circuit{\n"
        res = res + "---------- noeuds :\n"
        for n in self.noeuds :
            res = res + str(n) + "\n"
        res = res + "---------- composants :\n"
        for c in self.composants :
            res = res + f"{c.depart} {c} {c.arrivee}\n"
        res = res + "}"
        return res

    def composAdjacents(self,n : 'Noeud') -> list['Composant']:
        res = []
        for compo in self.composants :
            if compo.depart == n or compo.arrivee == n :
                res.append(compo)
        return res

    def chemins(self,nd : 'Noeud',na : 'Noeud',composVus : list['Composant']) -> list[list['Composant']] :
        """ trouve un chemin entre nd et na sans passer par les composants composVus"""
        if nd == na :
            return [[]]
        else :
            res = []
            for compo in self.composAdjacents(nd) :
                if compo not in composVus :
                    n2 = compo.noeudOppose(nd)
                    res = res + [[compo] + cheminRestant for cheminRestant in self.chemins(n2,na,composVus+[compo]) ]
            return res

    def affChemin(self,nd : 'Noeud',chemin : list['Composant']) -> str :
        if not chemin :
            return "[]"
        else :
            nextNoeud = nd
            res = f"[{nd}"
            for compo in chemin :
                nextNoeud = compo.noeudOppose(nextNoeud)
                res = res + f" {compo} {nextNoeud}"
            return res + "]"

    def mailles(self) -> list[list['Composant']]:
        """trouve les mailles du circuit
        On peut partir d'un noeud n1 quelconque du circuit (par exemple le premier)
        puis chercher les chemins partant de n1 et retournant à n1
        Petit détail : si je cherche directement les chemins de n1 à n1, j'obtient le chemin vide
        je suis donc obligé de forcer le passage sur les composants adjacents (faire un premier pas)
        avant d'utiliser la méthode chemins
        """
        n1 = self.noeuds[0]
        res = []
        for compo in self.composAdjacents(n1) :
            res = res + [[compo] + cheminRestant for cheminRestant in self.chemins(compo.noeudOppose(n1),n1,[compo]) ]
        return res


    def unCheminEnListeBinaire(self,chemin : list['Composant']) -> list['EntierMod2']:
        """
          . en numérotant les composants en fonction de leur place dans la liste des
            composants
          . on place en position j du résultat
             . EntierMod2(1) si j'ième composant apparait pas dans le chemin
             . EntierMod2(0) sinon
        :param chemins:
        :return:
        """
        res = [syslinZMod2.EntierMod2(0) for i in range(len(self.composants))]
        for i in range(len(self.composants)) :
            if self.composants[i] in chemin :
                res[i] = syslinZMod2.EntierMod2(1)
        return res

    def cheminsEnListeBinaires(self,chemins : list[list['Composant']]):
        return [self.unCheminEnListeBinaire(chemin) for chemin in chemins]


    def baseDeMailles(self) -> list[list['Composant']]:
        """
        la méthode trouvesMailles trouve TROP de mailles
        il nous faut un ensemble de mailles INDEPENDANTES
        Pour cela, on va considérer les mailles comme un ensemble de composants (on perd
        l'information de quel composant "suit" quel composant, mais ce n'est pas grave
        pour déterminer les mailles indépendantes)
        On remarque que la composition m3 de deux mailles m1 et m2 telle que :
           - m3 contient les mailles apparaissant dans m1 OU m2 mais n'apparaissant pas dans m1 ET m2
           (donc l'ensemble des mailles apparaissant dans m1 OU EXCLUSIF m2
        si m1 et m2 sont bien des mailles, alors m3 est également une maille
        Il nous faut donc déterminer un ensemble de vecteurs indépendants sur le corps (E,+2,*2) des entiers modulo 2 défini
        par les opérations :
           . E = {0,1}
           . x +2 y = (x + y) modulo 2   (c'est aussi le OU EXCLUSIF si l'on interprete 0/1 comme vrai/faux
           . x *2 y = x * y              (c'est aussi le ET si l'on interprete 0/1 comme vrai/faux

        Malheureusement, je n'ai pas trouvé de programme déjà fait en python pour travailler sur ce corps
        (cela doit exister, mais je n'ai pas l'impression que ce soit facile ni avec numpy ni avec sympy)
        j'ai donc reprogrammer le pivot de gauss dans le module syslinZMod2 que j'utilise ici
        Vous pouvez regarder le module syslinZMod2 mais ce n'est pas indispensable

        :param mailles:
        :return:
        """
        mailles = self.mailles()
        enBin = self.cheminsEnListeBinaires(mailles)
        numLignesIndependantes = syslinZMod2.indicesLignesIndependantes(enBin, syslinZMod2.EntierMod2)
        return [mailles[numLignesIndependantes[i]] for i in range(len(numLignesIndependantes))]

    @classmethod
    def circuitSujet(cls) -> 'Circuit':
        n1 = Noeud("n1")
        n2 = Noeud("n2")
        n3 = Noeud("n3")
        n4 = Noeud("n4")
        g = Composant("G",n1,n2)
        r1 = Composant("R1",n2,n3)
        indu = Composant("L1",n3,n4)
        r2 = Composant("R2",n4,n1)
        c = Composant("C1",n3,n1)
        return Circuit([n1,n2,n3,n4],[g,r1,indu,r2,c])

    @classmethod
    def circuitTestMailles(cls) -> 'Circuit':
        """
        un circuit avec quelques mailles de plus
        5 noeuds 1-5, 8 composants : G + R1-R7
        3----R1----4
        |\        /|
        | \      / |
        | R3    R4 |
        |   \  /   |
        G     1    R2
        |   /  \   |
        |  R7  R5  |
        | /      \ |
        2----R6----5
        pour l'instant que des résistances
        :return:
        """
        n1 = Noeud("n1")
        n2 = Noeud("n2")
        n3 = Noeud("n3")
        n4 = Noeud("n4")
        n5 = Noeud("n5")
        g = Composant("G",n2,n3)
        r1 = Composant("R1",n3,n4)
        r2 = Composant("R2",n4,n5)
        r3 = Composant("R3",n3,n1)
        r4 = Composant("R4",n4,n1)
        r5 = Composant("R5",n1,n5)
        r6 = Composant("R6",n2,n5)
        r7 = Composant("R7",n2,n1)
        return Circuit([n1,n2,n3,n4,n5],[g,r1,r2,r3,r4,r5,r6,r7])


if __name__ == '__main__':
    circuit = Circuit.circuitTestMailles()
    print(circuit)
    mailles = circuit.mailles()
    print("----- Mailles ------")
    for m in mailles :
        print(circuit.affChemin(circuit.noeuds[0],m))
    print("----- Base de Mailles ------")
    base = circuit.baseDeMailles()
    for m in base :
        print(circuit.affChemin(circuit.noeuds[0],m))
