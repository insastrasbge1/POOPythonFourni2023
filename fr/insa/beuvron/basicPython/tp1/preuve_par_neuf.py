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

def preuveParNeuf1():
    print("entrez un entier naturel : ")
    n = int(input())
    s = n
    while s > 9 :
        curs = 0
        while s > 0 :
            curs = curs + s % 10
            s = s // 10
        s = curs
    print(f"{n} --> {s}")

def preuveParNeuf2():
    print("entrez un entier naturel : ")
    n = int(input())
    s = n
    while s > 9 :
        s = s//10 + s % 10
    print(f"{n} --> {s}")

if __name__ == '__main__':
    preuveParNeuf1()
    preuveParNeuf2()
