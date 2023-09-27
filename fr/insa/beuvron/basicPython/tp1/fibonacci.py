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

def fibonacci():
    print("entrez un entier naturel : ")
    n = int(input())
    if n == 0 :
        fn1 = 0
    else :
        fn = 0
        fn1 = 1
        for i in range (2,n+1) :
            temp = fn
            fn = fn1
            fn1 = fn1 + temp
    print(f"fibo({n}) = {fn1}")

if __name__ == '__main__':
    fibonacci()
