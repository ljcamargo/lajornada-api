# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime as dayt
import constants as const
from collections import defaultdict
import math

class Zeitung(object):

    def __init__(self, action="", month="", year=""):
        self.action = action if action != None else ""
        self.month = month if month != None else ""
        self.year = year if year != None else ""
        self.json = "" 
        self.jsonr = ""
        self.html = ""
        self.globalJsonCloud()
      
    def getJsonHeuristicMonth(self):
        if len(self.month) < 2:
            self.month = "0"+self.month     
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '.json'     
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
            return True
        else:
            print "filenotfound "+filename
            return False
        
    def getJsonHeuristicYear(self):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '.json'     
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
            return True
        else:
            print "filenotfound "+filename
            return False
            
    def runRequest(self, isYear):
        mjson = json.loads(self.json,'utf-8')
        oddity =  mjson["oddity"]
        incidence =  mjson["incidence"]        
        html_i = "<br/><br/>"
        html_o = "<br/><br/>"
        for k,v in incidence.iteritems():
            if v>7:
                ev = 1+math.log10(v)
                html_i+= '<p class="inc" style="font-size:'+str(ev)+'em;">'+k+'</p>'
        for k,v in oddity.iteritems():
            if v>12:
                ev = 1+math.log10(v)
                html_o+= '<p class="ent" style="font-size:'+str(ev)+'em;">'+k+'</p>'
        if isYear:
            self.html += '<div class="item_block"><h1>'+self.year+'</h1><br/>'+ html_i + html_o
        else:
            self.html += '<div class="item_block"><h2>'+self.month+'/'+self.year+'</h2><br/>'+ html_i + html_o
    
    def startHTML(self):
        self.html = '<html><head><title>La Jornada</title></head><link rel="stylesheet" href="cloud.css"/><body><div class="main">'
    
    def endHTML(self):
        self.html += '</div></body></html>'
             
    def dumpHTML(self):
        filename = const.SAVING_ROUTE + '/cloud.html'
        f = open(filename, 'w')
        f.write(self.html)
        f.close()
        
    def globalJsonCloud(self):
        self.startHTML()
        self.jYears = defaultdict(int)
        for y in range (2012,2013):
            self.year = str(y)
            self.getJsonHeuristicYear()
            self.runRequest(True)
            for m in range (1,13):
                self.month = str(m)
                self.getJsonHeuristicMonth()
                self.runRequest(False)
        self.endHTML()
        self.dumpHTML() 
    
                 
if __name__ == '__main__':
    Zeitung()
    
    
            
            

 

     
        
        