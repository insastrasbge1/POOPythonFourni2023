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
from math import cos, sin


def convPolRec():
    print("conversion complexe polaire -> rectangulaire")
    print("entrez le module : ")
    r = float(input())
    print("entrez l'argument' : ")
    theta = float(input())
    a = r * cos(theta)
    b = r * sin(theta)
    print(f"{r} * exp({theta}) = {a} +i {b}")

def convPolRecPol():
    print("conversion complexe rectangulaire -> polaire")
    print("entrez la partie réelle : ")
    a = float(input())
    print("entrez la partie imaginaire : ")
    b = float(input())
    r = (a**2 + b**2) ** 0.5
    print(f"{r} * exp({theta}) = {a} +i {b}")

if __name__ == '__main__':
    convPolRec()
