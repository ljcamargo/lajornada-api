# -*- coding: utf-8 -*-
'''
Created on 13/05/2012

@author: lcammx
'''
from impresa import Impresa
from indexation import Indexation
          
               
if __name__ == '__main__':
    syear = '2010'
    for x in range(1,13):
        print "gen "+syear + "/" + str(x)
        Indexation("month", year=syear, month=str(x))
    syear = '2011'
    for x in range(1,13):
        print "gen "+syear + "/" + str(x)
        Indexation("month", year=syear, month=str(x))
    syear = '2012'
    for x in range(1,13):
        print "gen "+syear + "/" + str(x)
        Indexation("month", year=syear, month=str(x))