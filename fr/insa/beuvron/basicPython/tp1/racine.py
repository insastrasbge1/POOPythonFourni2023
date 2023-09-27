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

def racine():
    print("entrez un nombre positif : ")
    a = float(input())
    xn = (1+a) / 2
    xn1 = (xn + a/xn) / 2
    while abs((xn1-xn)/xn) > 1e-5 :
        xn = xn1
        xn1 = (xn + a/xn) / 2
    print(f"racide de {a} ~ {xn1}")
    print(f"a^(1/2) = {a**0.5} ; diff = {xn1 - a**0.5}")

if __name__ == '__main__':
    racine()
