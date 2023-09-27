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

class Rationnel :
    __slots__ = ("num","denom")

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

def reduire(r : Rationnel) -> Rationnel :
    p = pgcd(r.num,r.denom)
    res = Rationnel()
    res.num = r.num // p
    res.denom = r.denom // p
    if res.denom < 0 :
        res.num = - res.num
        res.denom = - res.denom
    return res

def cree(num : int , denom : int) -> Rationnel :
    res = Rationnel()
    res.num = num
    res.denom = denom
    return reduire(res)

def demande() -> Rationnel :
    print("numérateur ?")
    num = int(input())
    print("denominateur ?")
    denom = int(input())
    return cree(num,denom)

def aff(r : Rationnel) -> str :
    return f"{r.num}/{r.denom}"

def plus(r1 : Rationnel , r2 : Rationnel) -> Rationnel :
    pg = pgcd(r1.denom,r2.denom)
    res = Rationnel()
    res.num = r1.num * (r2.denom // pg) + r2.num * (r1.denom // pg)
    res.denom = ppcm(r1.denom,r2.denom)
    return reduire(res)

def opp(r : Rationnel) -> Rationnel :
    res = Rationnel()
    res.num = - r.num
    res.denom = r.denom
    return res

def moins(r1 : Rationnel , r2 : Rationnel) -> Rationnel :
    return plus(r1,opp(r2))

def mult(r1 : Rationnel , r2 : Rationnel) -> Rationnel :
    pg1 = pgcd(r1.num,r2.denom)
    pg2 = pgcd(r1.denom,r2.num)
    res = Rationnel()
    res.num = (r1.num // pg1) * (r2.num // pg2)
    res.denom = (r1.denom // pg2) * (r2.denom // pg1)
    return reduire(res)

def inv(r : Rationnel) -> Rationnel :
    if r.num == 0 :
        raise ZeroDivisionError()
    res = Rationnel()
    if r.num > 0 :
        res.num = r.denom
        res.denom = r.num
    else :
        res.num = - r.denom
        res.denom = - r.num
    return res

def div(r1 : Rationnel , r2 : Rationnel) -> Rationnel :
    return mult(r1,inv(r2))

def determinant(a11 : Rationnel , a12 : Rationnel
                , a21 : Rationnel , a22 : Rationnel) -> Rationnel :
    return moins(mult(a11,a22),mult(a12,a21))

def resoud(a1 : Rationnel, b1 : Rationnel, c1 : Rationnel
           , a2 : Rationnel, b2 : Rationnel, c2 : Rationnel) -> tuple[Rationnel] :
    det = determinant(a1,b1,a2,b2)
    if det.num == 0 :
        return ()
    else :
        x = div(determinant(c1,b1,c2,b2),det)
        y = div(determinant(a1,c1,a2,c2),det)
        return (x,y)

def testResoud() -> None :
    print("resolution système 2 équations 2 inconnues dans les rationnels")
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
    if res == () :
        print("determinant nul : aucune ou une infinité de solutions")
    else :
        print(f"x = {aff(res[0])} ; y = {aff(res[1])}")

if __name__ == '__main__':
    testResoud()
