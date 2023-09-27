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

def sommeEntier() :
    print("entrez un entier naturel : ")
    n = int(input())
    i = 1
    s = 0
    while i <= n :
        s = s + i
        i = i + 1
    print(f"somme avec while : {s}")
    s = 0
    for i in range(1,n+1) :
        s = s + i
    print(f"somme avec for : {s}")

if __name__ == '__main__':
    sommeEntier()