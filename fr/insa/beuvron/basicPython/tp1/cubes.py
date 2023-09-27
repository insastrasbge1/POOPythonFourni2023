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

def cubes1():
    for n in range(2,1001) :
        r = n
        somme_cube = 0
        while r > 0 :
            somme_cube = somme_cube + (r % 10) ** 3
            r = r // 10
        if somme_cube == n :
            print(n)

def cubes2():
    for c in range(0,10) :
        for d in range(0,10) :
            for u in range(0,10) :
                n = 100*c + 10*d + u
                if n >= 2 and c**3 + d**3 + u**3 == n :
                    print(100*c + 10*d + u)

if __name__ == '__main__':
    cubes1()
    cubes2()
