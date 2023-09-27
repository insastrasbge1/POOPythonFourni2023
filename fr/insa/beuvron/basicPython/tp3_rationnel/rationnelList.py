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


def pgcd(u : int , v : int) -> int :
    u = abs(u)
    v = abs(v)
    while v != 0 :
        temp = u
        u = v
        v = temp % v
    return u

def ppcm(u : int , v : int) -> int :
    return u * (v // pgcd(u,v))

def reduire(r : list) -> list :
    p = pgcd(r[0],r[1])
    res = [r[0] // p, r[1] // p]
    if res[1] < 0 :
        res[0] = - res[0]
        res[1] = - res[1]
    return res

def cree(num : int , denom : int) -> list :
    res = (num,denom)
    return reduire(res)

def demande() -> list :
    print("numérateur ?")
    num = int(input())
    print("denominateur ?")
    denom = int(input())
    return cree(num,denom)

def aff(r : list) -> str :
    return f"{r[0]}/{r[1]}"

def plus(r1 : list , r2 : list) -> list :
    pg = pgcd(r1[1],r2[1])
    res = [0,0]
    res[0] = r1[0] * (r2[1] // pg) + r2[0] * (r1[1] // pg)
    res[1] = ppcm(r1[1],r2[1])
    return reduire(res)

def opp(r : list) -> list :
    return [- r[0],r[1]]

def moins(r1 : list , r2 : list) -> list :
    return plus(r1,opp(r2))

def mult(r1 : list , r2 : list) -> list :
    pg1 = pgcd(r1[0],r2[1])
    pg2 = pgcd(r1[1],r2[0])
    res = [0,0]
    res[0] = (r1[0] // pg1) * (r2[0] // pg2)
    res[1] = (r1[1] // pg2) * (r2[1] // pg1)
    return reduire(res)

def inv(r : list) -> list :
    if r[0] == 0 :
        raise ZeroDivisionError()
    return reduire([r[1],r[0]])

def div(r1 : list , r2 : list) -> list :
    return mult(r1,inv(r2))

def determinant(a11 : list , a12 : list
                , a21 : list , a22 : list) -> list :
    return moins(mult(a11,a22),mult(a12,a21))

def resoud(a1 : list, b1 : list, c1 : list
           , a2 : list, b2 : list, c2 : list) -> None | tuple[list, list]:
    det = determinant(a1,b1,a2,b2)
    if det[0] == 0 :
        return None
    else :
        x = div(determinant(c1,b1,c2,b2),det)
        y = div(determinant(a1,c1,a2,c2),det)
        return (x,y)

def testResoud() -> None :
    print("resolution système 2 équations 2 inconnues dans les lists")
    print("{ a1 x + b1 y = c1")
    print("{ a2 x + b2 y = c2")
    print("a1 ?")
    a1 = demande()
    print("b1 ?")
    b1 = demande()
    print("c1 ?")
    c1 = demande()
    print("a2 ?")
    a2 = demande()
    print("b2 ?")
    b2 = demande()
    print("c2 ?")
    c2 = demande()
    res = resoud(a1,b1,c1,a2,b2,c2)
    if res == None :
        print("determinant nul : aucune ou une infinité de solutions")
    else :
        print(f"x = {aff(res[0])} ; y = {aff(res[1])}")

if __name__ == '__main__':
    testResoud()
