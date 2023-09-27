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

def jeu421():
    s = 0
    for d1 in range(1,7) :
        for d2 in range(1, 7):
            for d3 in range(1, 7) :
                if d1 < d2 :
                    if d1 < d3 :
                        dmin = d1
                        if d2 < d3 :
                            dmoy = d2
                            dmax = d3
                        else :
                            dmoy = d3
                            dmax = d2
                    else :
                        dmax = d2
                        dmoy = d1
                        dmin = d3
                else :
                    if d2 < d3 :
                        dmin = d2
                        if d1 < d3 :
                            dmoy = d1
                            dmax = d3
                        else :
                            dmoy = d3
                            dmax = d1
                    else :
                        dmin = d3
                        dmoy = d2
                        dmax = d1
                n = 100*dmax + 10*dmoy + dmin
                if n == 421 :
                    g = 8
                elif n == 111 :
                    g = 7
                elif dmoy == 1 and dmin == 1 :
                    g =  dmax
                elif dmax == dmoy and dmoy == dmin :
                    g =  dmax
                elif dmax == dmoy + 1 and dmoy == dmin + 1 :
                    g =  2
                else :
                    g =  1
                # print(f"{d1} {d2} {d3} -> {dmax} {dmoy} {dmin} : {g}")
                s = s + g
    print(f"somme des gains : {s}")
    print(f"esperance : {s/6**3}")

if __name__ == '__main__':
    jeu421()
