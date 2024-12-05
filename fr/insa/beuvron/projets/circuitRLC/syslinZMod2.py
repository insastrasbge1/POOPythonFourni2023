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
Created on 2022-07-03

ni numpy ni sympy ne semble fonctionner avec le corps des entiers modulo 2
je refais la méthode de gauss pour pouvoir déterminer les lignes indépendantes
d'une matrice
@author: Francois de Bertrand de Beuvron
"""
from typing import List, Any


class EntierMod2() :
    """
    le corps des entier modulo 2 avec les opérations +,* :
    + | 0 | 1 |
    --+---+---+
    0 | 0 | 1 |
    --+---+---+
    1 | 1 | 0 |
    --+---+---+

    * | 0 | 1 |
    --+---+---+
    0 | 0 | 0 |
    --+---+---+
    1 | 0 | 1 |
    --+---+---+
    (peut être également vu comme le corps des booléens avec les opération XOR et AND)
    """
    def __init__(self,val : int = 0):
        if val != 0 and val != 1 :
            raise Exception("only 0 or 1")
        self._val = val

    def __add__(self, other : 'EntierMod2') -> 'EntierMod2':
        return EntierMod2((self._val + other._val) % 2)

    def __pos__(self) -> 'EntierMod2':
        return self

    def __neg__(self) -> 'EntierMod2':
        return EntierMod2(self._val)

    def __sub__(self, other) -> 'EntierMod2':
        return self.__add__(other.__neg__())

    def __mul__(self, other) -> 'EntierMod2':
        return EntierMod2(self._val * other._val)

    def __invert__(self) -> 'EntierMod2':
        if self._val == 0 :
            raise Exception("division par zero")
        return self

    def __truediv__(self, other : 'EntierMod2') -> 'EntierMod2':
        return self.__mul__(other.__invert__())

    def __eq__(self, other) -> bool:
        if isinstance(other,self.__class__) :
            return self._val == other._val
        else :
            return False

    def __str__(self):
        return str(self._val)

    @classmethod
    def ZERO(cls) -> 'EntierMod2':
        return EntierMod2(0)

class PermutationInt():
    """
    une petite classe utilitaire permettant de représenter les permutations
    sur l'ensemble {0,...,taille-1}
    Cela va nous permettre de représenter des permutations de lignes/colonnes d'une matrice
    sans permuter effectivement les coefficients
    """
    def __init__(self,taille : int):
        self._taille = taille
        # j'initialise avec la permutation identité
        self._permut = [i for i in range(taille)]

    @property
    def taille(self):
        return self._taille

    def perm(self,i : int) -> int:
        """
        :return: perm(i)
        """
        return self._permut[i]

    def permutte(self,i : int,j : int) -> None:
        """
        compose la permutation courante en ajoutant la permutation
        des entiers perm(i) et perm(j)
        """
        #
        old = self._permut[i]
        self._permut[i] = self._permut[j]
        self._permut[j] = old


def affList(ch : list['object']) -> str:
    return "[" + ",".join([str(compo) for compo in ch]) + "]"

def affMat(lch : list[list['object']]) -> str:
        return "[" + ",\n".join([affList(ch) for ch in lch]) + "]"

def affMatPerm(mat : list[list['object']],permLig : PermutationInt,permCol : PermutationInt) -> str:
    if len(mat) == 0 :
        return "[]"
    else :
        nbrLig = len(mat)
        nbrCol = len(mat[0])
        matPerm = [[mat[permLig.perm(lig)][permCol.perm(col)] for col in range(nbrCol)] for lig in range(nbrLig)]
        return affMat(matPerm)

def pivotGauss(mat : list[list['corps']],corps : type,
                permLig : PermutationInt,permCol : PermutationInt) -> int :
    """
    Cette fonction peut être utilisée comme base de nombreux calculs.

    * soit une matrice mat sur un corps :
    Un corps est une classe qui définie :
        les méthodes d'instance :
            __add__, __sub__, __mul__ , __truediv__ pour les opérateurs + - * /
            __eq__ pour l'opérateur ==
        les méthodes de classe :
            ZERO() renvoyant l'élément neutre de __add__

    * La matrice est représentée par une liste de liste.
    On suppose que toutes les listes ont la même taille.
    on note nbrLig et nbrCol le nombre de lignes/colonnes de la matrice

    * cette matrice a éventuellement subit des permutations de lignes et de
    colonnes, représentées par permLig et permCol

    * Cette méthode modifie la matrice pour la rendre triangulaire supérieure
    avec des éventuelles nouvelles permutations de lignes et colonnes (pivot total)

    * Elle renvoie r : le nombres de lignes indépendantes

    * elle modifie permLig et perCol pour s'assurer que :
        _ la sous-matrice avec les lignes :
            permLig[0],permLig[1],..,permLig[r-1]
        et les colonnes :
            permCol[0],permCol[1],..,permCol[r-1]
        est triangulaire supérieure
        - toutes les lignes permLig[r],permLig[r+1],..,permLig[nbrLig-1]
          sont 'nulle' : tous les coefficients sont nuls

    """
    if len(mat) == 0 :
        return 0
    else :
        etape = 0;
        nbrLig = len(mat)
        # on suppose que toutes les lignes ont le même nombre de colonnes
        nbrCol = len(mat[0])
        trouve = True
        while trouve and etape < nbrCol:
            # trouve un pivot non nul si possible
            # print(f"etape : {etape}")
            # print(f"mat = \n{affMatPerm(mat, permLig, permCol)}")
            lig = etape
            col = etape
            trouve = False
            while col < nbrCol and trouve == False :
                lig = etape
                while lig < nbrLig and trouve == False :
                    if not (mat[permLig.perm(lig)][permCol.perm(col)] == corps.ZERO()) :
                        trouve = True
                    else :
                        lig += 1
                if not trouve :
                    col += 1
            # je ne continue que si j'ai trouvé une ligne/col avec un pivot non nul
            if trouve :
                # je permute les lignes et colonnes
                # print(f"pivot : ({lig},{col})")
                permLig.permutte(etape,lig)
                permCol.permutte(etape,col)
                for i in range(etape+1,nbrLig):
                    if not (mat[permLig.perm(i)][permCol.perm(etape)] == corps.ZERO()) :
                        pivot = mat[permLig.perm(i)][permCol.perm(etape)] / mat[permLig.perm(etape)][permCol.perm(etape)]
                        # print(f"pivot = {pivot}")
                        mat[permLig.perm(i)][permCol.perm(etape)] = corps.ZERO()
                        for j in range(etape+1,nbrCol):
                            # print(f"old[{permLig.perm(i)},{permCol.perm(j)}] : {mat[permLig.perm(i)][permCol.perm(j)]}")
                            mat[permLig.perm(i)][permCol.perm(j)] = mat[permLig.perm(i)][permCol.perm(j)] - \
                                                          mat[permLig.perm(etape)][permCol.perm(j)]*pivot
                            # print(f"new[{permLig.perm(i)},{permCol.perm(j)}] : {mat[permLig.perm(i)][permCol.perm(j)]}")

                etape += 1
        return etape

def fromIntToEntierMod2(mat : list[list[int]]) -> list[list[EntierMod2]] :
    return [[EntierMod2(val) for val in ligne] for ligne in mat]

def indicesLignesIndependantes(mat : list[list['corps']],corps : type) -> list[int] :
    """
    renvoie la liste des indices des lignes indépendantes
    :param mat:
    :return:
    """
    if len(mat) == 0 :
        return 0
    else :
        permLig = PermutationInt(len(mat))
        permCol = PermutationInt(len(mat[0]))
        nbr = pivotGauss(mat,corps,permLig,permCol)
        # print(nbr)
        return [permLig.perm(i) for i in range(nbr)]

def lignesIndependantes(mat : list[list['corps']],corps : type) -> list[list['corps']]:
    """
    renvoie la matrice des lignes indépendantes
    """
    if len(mat) == 0 :
        return mat
    else :
        permLig = PermutationInt(len(mat))
        permCol = PermutationInt(len(mat[0]))
        nbr = pivotGauss(mat,corps,permLig,permCol)
        return [mat[permLig.perm(i)] for i in range(nbr)]

def testLignesIndependantes1() :
    mat = [ [EntierMod2(1),EntierMod2(1)] ,
            [EntierMod2(1), EntierMod2(0)]]
    res = indicesLignesIndependantes(mat,EntierMod2)
    print(res)

def testLignesIndependantes2() :
    """
    mailles : {[R4,R2,R6,G,R3],[R5,R6,G,R3],[R7,G,R3],[R5,R2,R4,R7,G,R3],
    [R4,R2,R5,R7,G,R3],[R4,R2,R6,R1,R3],[R5,R6,R1,R3],[R7,R1,R3]}

    En binaire :
    [[1,0,1,1,1,0,1,0],
[1,0,0,1,0,1,1,0],
[1,0,0,1,0,0,0,1],
[1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1],
[0,1,1,1,1,0,1,0],
[0,1,0,1,0,1,1,0],
[0,1,0,1,0,0,0,1]]
    :return:
    """
    mat = fromIntToEntierMod2([[1,0,1,1,1,0,1,0],
[1,0,0,1,0,1,1,0],
[1,0,0,1,0,0,0,1],
[1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1],
[0,1,1,1,1,0,1,0],
[0,1,0,1,0,1,1,0],
[0,1,0,1,0,0,0,1]])
    res = indicesLignesIndependantes(mat,EntierMod2)
    print(res)

def testLignesIndependantes3() :
    """
    avec les mailles "de base"
    mailles : {[R3,R1,R4],[R4,R2,R5],[R5,R6,R7],[R7,G,R3]}

    En binaire :
    [[0,1,0,1,1,0,0,0],
[0,0,1,0,1,1,0,0],
[0,0,0,0,0,1,1,1],
[1,0,0,1,0,0,0,1]]
    :return:
    """
    mat = fromIntToEntierMod2([
        [0,1,0,1,1,0,0,0],
        [0,1,0,1,1,0,0,0],  # doublée
        [0,0,1,0,1,1,0,0],
        [0,1,1,1,0,1,0,0],  # redondante deux précédentes
        [0,0,0,0,0,1,1,1],
        [1,0,0,1,0,0,0,1]])
    indices = indicesLignesIndependantes(mat,EntierMod2)
    print(f"indices : {indices}")
    lignes = lignesIndependantes(mat,EntierMod2)
    print(f"lignes : \n{formatMatrix(lignes)}")

def formatMatrix(mat : list[list['corps']]) -> str :
    return '\n'.join([' '.join(map(str,ligne)) for ligne in mat])

if __name__ == '__main__':
    # testLignesIndependantes1()
    testLignesIndependantes3()