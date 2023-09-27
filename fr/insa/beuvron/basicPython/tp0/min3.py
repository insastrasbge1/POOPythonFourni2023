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

def min3_v1() :
    print("entrez un premier entier")
    a = int(input())
    print("entrez un deuxième entier")
    b = int(input())
    print("entrez un troisième entier")
    c = int(input())
    if a > b :
        temp = a
        a = b
        b = temp
    if a > c :
        temp = a
        a = c
        c = temp
    if b > c :
        temp = b
        b = c
        c = temp
    print(f"{a} <= {b} <= {c}")

def min3_v2() :
    print("entrez un premier entier")
    d1 = int(input())
    print("entrez un deuxième entier")
    d2 = int(input())
    print("entrez un troisième entier")
    d3 = int(input())
    if d1 < d2:
        if d1 < d3:
            dmin = d1
            if d2 < d3:
                dmoy = d2
                dmax = d3
            else:
                dmoy = d3
                dmax = d2
        else:
            dmax = d2
            dmoy = d1
            dmin = d3
    else:
        if d2 < d3:
            dmin = d2
            if d1 < d3:
                dmoy = d1
                dmax = d3
            else:
                dmoy = d3
                dmax = d1
        else:
            dmin = d3
            dmoy = d2
            dmax = d1
    print(f"{d1} {d2} {d3} -> {dmax} {dmoy} {dmin}")


if __name__ == '__main__':
    min3_v1()
    min3_v2()