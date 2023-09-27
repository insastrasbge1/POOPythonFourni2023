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

def affDuree() :
    print("entrez un entier (durée en ms)")
    tms = int(input())
    if tms < 1000 :
        print(f"{tms} ms")
    else :
        ms = tms % 1000
        tsec = tms // 1000
        if tsec < 60 :
            print(f"{tsec}.{ms} s")
        else :
            sec = tsec % 60
            tmin = tsec // 60
            if tmin < 60 :
                print(f"{tmin} mn {sec} s")
            else :
                mn = tmin % 60
                th = tmin // 60
                print(f"{th} h {mn} mn")


if __name__ == '__main__':
    affDuree()