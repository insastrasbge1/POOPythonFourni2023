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
determiner une base de mailles (ensemble de mailles indépendantes)
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

on représente les mailles par un vecteur de même taille que le nombre de composant
la composante i du vecteur vaut 1 si le composant i appartient à la maille, 0 sinon
exemple la maille [1,1,0,0,1] est la maille G-R1-C1

Le calcul des mailles du circuit fera l'objet d'un TD.
Le problème est que l'on obtient en général de trop nombreuses mailles qui ne sont pas
indépendantes. Dans notre exemple (n'hesitez pas à dessiner le circuit pour vous en rendre compte),
on "voit" tout de suite les mailles :
G-R1-C1 = [1,1,0,0,1]
L1-R2-C1 = [0,0,1,1,1]
G-R1-L1-R2 = [1,1,1,1,0] est également une maille
Mais ces trois mailles ne sont pas indépendante dans le sens ou si je combine les deux premières,
j'obtient la dernière
Pour avoir le bon nombre d'équations correspondant à la loi de mailles, il faut que je
travaille sur un ensemble de mailles indépendantes. Si je représente l'ensemble des mailles par
une matrice (une ligne par maille) :
[1,1,0,0,1]
[0,0,1,1,1]
[1,1,1,1,0]
il me faut déterminer un ensemble maximal de lignes indépendantes.
la methode rref de sympy permet de déterminer cela pour les types supportés par sympy
par exemple des flottants ou des complexes, mais pas pour des classes définies par
l'utilisateur.
Or nous voulons travailler sur un corps spécifique : quand je combine des mailles,
si je passe deux fois par un même composant, ce composant n'est plus dans la maille
résultat.
On veut donc utiliser le corps des entiers modulo 2 (Z/2Z,+,*) que l'on peut voir
aussi comme le corp des booléens ({vrai,faux},XOR,AND)
Je n'ai pas trouvé de module python correspondant. Je l'ai donc programmé dans le module
syslinZMod2
Ici, on ne fait que l'utiliser
"""
import sympy.core.numbers
from sympy.matrices import Matrix

from fr.insa.beuvron.projets.circuitRLC.syslinZMod2 import formatMatrix,EntierMod2,fromIntToEntierMod2,lignesIndependantes

def testSympy() -> None :
    """
    On aurait aimé le faire avec sympy, mais NON
    premier exemple repris de https://stackoverflow.com/questions/58293353/how-do-i-reduce-a-matrix-to-row-echelon-form-using-numpy
    """
    m = Matrix([
            [.85, -.15, -.7, 0, 0],
            [-.15, .8, -.4, -.25, 0],
            [-.1, -.1, .45, -.25, 0],
            [-.25, -.1, -.4, .75, 0]])
    M_rref = m.rref()
    print(f"matrice flottants : {M_rref}")
    ml = [[1,1,0,0,1],[0,0,1,1,1],[1,1,1,1,0]]
    # rref détermine les vecteurs colonnes indépendants
    # puisque l'on veut les lignes indépendantes, on transpose la matrice m.T en sympy
    mi = Matrix(ml).T  # ok : matrice d'int
    mir = mi.rref()    # ok, mais l'indépendance dans Z n'est pas l'indépendance dans Z/2Z (Z mod 2)
    print(f"matrice int : {mir}")
    me = Matrix(fromIntToEntierMod2(ml)).T  # gros warning en fait il a re-transformé
    print(f"type dans Matrix : {type(me[0,0])}")  #  en sympy.core.numbers.One
    print(f"type dans Matrix : {type(me[0,1])}")  #  ou sympy.core.numbers.Zero
    mer = me.rref()                         # et toujours pas le résultat escompté
    print(f"matrice EntierMod2 : {mer}")
    zero = sympy.core.numbers.Zero()
    print(f"zero sympy : {zero}")
    one = sympy.core.numbers.One()
    print(f"one + one = {one+one}")   # fait l'addition des int
    print(f"type(one + one) = {type(one+one)}")

def testBaseMaille() -> None :
    matMaillesEntiersNormaux = [[1,1,0,0,1],[0,0,1,1,1],[1,1,1,1,0]]
    matMaillesEntierMod2 = fromIntToEntierMod2(matMaillesEntiersNormaux)
    print(f"mailles originales : \n{formatMatrix(matMaillesEntierMod2)}")
    lignesOK = lignesIndependantes(matMaillesEntierMod2,EntierMod2)
    print(f"mailles apres gauss : \n{formatMatrix(matMaillesEntierMod2)}")
    print(f"base de mailles : \n{formatMatrix(lignesOK)}")

if __name__ == '__main__':
    testSympy()
    # testBaseMaille()
