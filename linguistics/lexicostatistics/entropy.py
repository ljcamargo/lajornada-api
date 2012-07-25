# -*- coding: utf-8 -*-
'''
Created on 27/06/2012

@author: lcammx
'''
import re

class Entropy(object):


    def __init__(self, input):
        self.input = input
        self.aleph = ""
        self.beth = ""
        self.gamal = ""
        self.dalat = ""
        self.he = ""
        self.waw = ""
        self.zayn = ""
        self.het = ""
        self.measureEntropy()
        
    def measureEntropy(self):
        for c in self.input:
            self.aleph += '1' if (c!=' ') else '0'  #SPACES
            self.beth += '1' if (re.match("[A-Z]", c)) else '0' #MAYUS
            self.gamal += '1' if (re.match(r'[áéíóú]', c)) else '0' #ACCUTED
            self.dalat += '1' if (re.match(r'[aeiáéí]', c)) else '0' # fron vow
            self.he += '1' if (re.match(r'[iuíú]', c)) else '0' # cloed vow
            self.waw  += '1' if (re.match(r'[eoéó]', c)) else '0' # closed vow ctl
            self.zayn += '1' if (re.match(r'[mnljwrbdg]', c)) else '0' #voiced, lasting
            self.het += '1' if (re.match(r'[mbpvfdtlrnzs]', c)) else '0' #anatomy anterior
            #self.shin += '1' if (re.match(r'[mbpvfdtjgkxw]', c)) else '0' # anatomy anterior anterior
        print self.input
        print self.aleph
        print self.beth
        print self.gamal
        print self.dalat
        print self.he
        print self.waw
        print self.zayn
        print self.het;
            
            
                           
if __name__ == '__main__':
    txt = 'El gran murciélago feliz cabilante'
    Entropy(txt)

            