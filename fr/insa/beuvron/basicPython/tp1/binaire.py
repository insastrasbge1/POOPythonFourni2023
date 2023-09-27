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

def binaireInverse():
    print("entrez un entier naturel : ")
    n = int(input())
    if n == 0 :
        print(0)
    else :
        while n > 0 :
            print(n%2,end="")
            n = n // 2
        print()

def binaire() :
    print("entrez un entier naturel : ")
    n = int(input())
    if n == 0 :
        print(0)
    else :
        ordre = 1
        cur = n // 2
        while cur > 0 :
            ordre = ordre * 2
            cur = cur // 2
        print(f"ordre = {ordre}")
        while ordre > 0 :
            print(n//ordre,end="")
            n = n % ordre
            ordre = ordre // 2
        print()

if __name__ == '__main__':
    # binaireInverse()
    binaire()
