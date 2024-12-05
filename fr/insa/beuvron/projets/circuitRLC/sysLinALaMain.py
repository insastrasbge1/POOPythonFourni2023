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
Le but ici n'est qu'un exemple : à partir d'un circuit donné,
construire le système complexe correspondant et le resoudre
!!! normalement, la matrice et le second membre sont créés automatiquement
à partir du circuit
!!! c'est à faire dans le sujet, mais ce n'est pas donné ici
!!! ce module ne donne que des pistes
Nous partons du circuit exemple :
circuit courant :
Circuit{
---------- noeuds :
[Noeud n1 : 0,0]
[Noeud n2 : 0,100]
[Noeud n3 : 100,100]
[Noeud n4 : 100,0]
---------- composants :
[GenerateurTension G (n1 -> n2) : fem 10 Volt
[Resistance R1 (n2 -> n3) : 200 Ohm]
[Inductance L1 (n3 -> n4) : inductance 0.01 Henry]
[Resistance R2 (n4 -> n1) : 400 Ohm]
[Condensateur C1 (n3 -> n1) : capacite 0.0001 Farad]

Created on 2022-07-03

@author: Francois de Bertrand de Beuvron
"""

# pour l'utilisation des nombres complexes
import cmath
# pour la résolution d'un système linéaire (compatible avec les complexes)
# chargez les modules numpy et sympy
# il faut inclure le package numpy
import numpy
# sympy permet de déterminer un ensemble de vecteurs lignes indépendants
import sympy

class SyslinComplex():
    def __init__(self,mat : 'numpy.ndarray',secondMenmbre : numpy.ndarray):
        self._mat = mat
        self._secondMembre = secondMenmbre

    @property
    def mat(self):
        return self._mat

    @property
    def secondMembre(self):
        return self._secondMembre

    def __str__(self):
        res = "matrice : \n"
        res = res + str(self._mat)
        res = res + "\nsecond membre :"
        res = res + str(self._secondMembre)
        return res

    def solve(self) :
        return numpy.linalg.solve(self._mat,self._secondMembre)

def sysPourExempleCircuit(omega : float) -> SyslinComplex:
    """
    NOTE IMPORTANTE : j'ai fait cette construction à la main
    il est très possible que je me sois trompé
    ==> vérifiez, et merci de me signaler les erreurs

    le circuit :
    Circuit{
---------- noeuds :
[Noeud n1 : 0,0]
[Noeud n2 : 0,100]
[Noeud n3 : 100,100]
[Noeud n4 : 100,0]
---------- composants :
[GenerateurTension G (n1 -> n2) : fem 10 Volt
[Resistance R1 (n2 -> n3) : 200 Ohm]
[Inductance L1 (n3 -> n4) : inductance 0.01 Henry]
[Resistance R2 (n4 -> n1) : 400 Ohm]
[Condensateur C1 (n3 -> n1) : capacite 0.0001 Farad]

    la numérotation des inconnues :
    - 5 composants numérotés de 0 à 4 (dans l'ordre de la liste ci-dessus)
    - ==> 10 inconnues
      . la tension au borne du composant Ci est la variable N° 2*i
      . l'intensité traversant le composant Ci est la variable N° 2*i+1
    :return:
    """
    nbrComp = 5
    nbrInconnues = nbrComp * 2
    # la matrice du système est de taille 10*10
    # les coefficient sont initialisé avec des 0 complex
    mat = numpy.zeros((nbrInconnues,nbrInconnues),dtype=complex)
    secondMembre = numpy.zeros(nbrInconnues,dtype=complex)
    cj = complex(0,1)
    lig = 0
    #----------- loi d'Ohm
    # une équation par composant
    # générateur : U0 = fem + i 0 (on considère le déphase nul aux bornes du générateur)
    mat[lig,2*0] = complex(1,0)
    secondMembre[lig] = complex(10,0)
    lig = lig +1
    # resistance R1 : U1 - R1.I1 = 0
    mat[lig,2*1] = complex(1,0)
    mat[lig,2*1+1] = complex(-200,0)
    lig = lig +1
    # inductance L1 : U1 - j.L1.omega.I1 = 0
    mat[lig,2*2] = complex(1,0)
    mat[lig,2*2+1] = -cj*0.01*omega
    lig = lig +1
    # resistance R2 : U1 - R2.I1 = 0
    mat[lig,3*2] = complex(1,0)
    mat[lig,3*2+1] = complex(-400,0)
    lig = lig +1
    # condensateur C1 : U1 - 1/(j.C1.omega).I1 = 0
    mat[lig,4*2] = complex(1,0)
    mat[lig,4*2+1] = -1/(cj*0.0001*omega)
    lig = lig +1

    #----------- loi des noeuds
    # il y a 4 noeud, cela donne 3 equations
    # noeud 1 : I0 - I4 - I3 = 0
    mat[lig,2*0+1] = complex(1,0)
    mat[lig,2*4+1] = complex(-1,0)
    mat[lig,2*3+1] = complex(-1,0)
    lig = lig + 1
    # noeud 2 : - I0 + I1 = 0
    mat[lig,2*0+1] = complex(-1,0)
    mat[lig,2*1+1] = complex(1,0)
    lig = lig + 1
    # noeud 3 : -I1 + I4 + I2 = 0
    mat[lig,2*1+1] = complex(-1,0)
    mat[lig,2*4+1] = complex(1,0)
    mat[lig,2*2+1] = complex(1,0)
    lig = lig + 1

    #-------------- loi des mailles
    # à partir de la base de maille :
    # on représente les maille par un vecteur de même taille que le nombre de composant
    # la composante i du vecteur vaut 1 si le composant i appartient à la maille, 0 sinon
    # exemple la maille [1,1,0,0,1] est la maille G-R1-C1
    # la somme des tensions est nulle (en faisant attention aux signes)
    # pour déterminer une base de maille, voir le fichier maillesALaMain
    #  maille 1 : G-R1-C1 = [1,1,0,0,1]
    mat[lig,2*0] = complex(1,0)
    mat[lig,2*1] = complex(-1,0)
    mat[lig,2*4] = complex(-1,0)
    lig = lig + 1
    #  maille 1 : L1-R2-C1 = [0,0,1,1,1]
    mat[lig,2*2] = complex(1,0)
    mat[lig,2*3] = complex(1,0)
    mat[lig,2*4] = complex(-1,0)
    lig = lig + 1
    return SyslinComplex(mat,secondMembre)

def maillesRedondantesAsMatrixTest() :
    """
    pour avec le circuit : avec les composants numérotés dans l'ordre
    [GenerateurTension G (n1 -> n2) : fem 10 Volt
    [Resistance R1 (n2 -> n3) : 200 Ohm]
    [Inductance L1 (n3 -> n4) : inductance 0.01 Henry]
    [Resistance R2 (n4 -> n1) : 400 Ohm]
    [Condensateur C1 (n3 -> n1) : capacite 0.0001 Farad]
    En supposant que l'on a trouvé les mailles :
    [1 1 1 1 0 ] (-> maille G R1 L1 R2)
    [G

    sympy : trouve les colonnes indépendantes :
    M.columnspace()
    voir fin de https://stackoverflow.com/questions/28816627/how-to-find-linearly-independent-rows-from-a-matrix

    :return:
    """


if __name__ == '__main__':
    mat = numpy.zeros((2,2),dtype=complex)
    print(type(mat))
    secondMembre = numpy.zeros(2,dtype=complex)
    print(type(secondMembre))
    sys = sysPourExempleCircuit(100)
    print(sys)
    sol = sys.solve()
    print("solution : ")
    print(sol)
