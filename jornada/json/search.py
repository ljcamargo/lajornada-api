# -*- coding: utf-8 -*-

import json
import os
from linguistics.gramatics.esp import ESP as LANG
from linguistics.gramatics.heuristics import Heuristics
from datetime import datetime as dayt
from datetime import timedelta
import constants as const
from collections import defaultdict



class Search(object):

    def __init__(self, txt="", richness="html", source="impresa", detail="full"):
        self.DETAIL_NO_CONTENT = "nocontent"
        self.DETAIL_MINIMAL = "minimal"
        self.txt = txt if txt != None else ""
        self.richness = richness if (richness != None or richness == "") else "html"
        self.source = source if source != None else "impresa"
        self.detail = detail if detail != None else "full"
        self.json = "" 
        self.result = ""
        self.rWords = []
        self.rOddity = defaultdict(int)
        self.Abstracted = ""
          
        if not self.richness in ['html','plain','list','all']:
            self.richness = 'html'

        if not self.detail in ['nocontent','minimal','full']:
            self.detail = 'nocontent'
            
        self.preProcessSearchString(self.txt)
                                    
        self.getjsonGlobalIndex()
        if len(self.json)>1:
            self.runrequest()
        else:
            self.notbeenfound()
                    
    def preProcessSearchString(self, text):
        heur = Heuristics('esp')
        abstr = []
        heur._matchTextToList(text, self.rWords)
        heur._proccessOddness(text, self.rOddity)
        heur._processAbstraction(text, abstr)
        self.rWords = heur.makeAbstractList(self.rWords)
        self.Abstracted = "".join(abstr)
        print "words" + self.rWords.__str__()
        print self.rOddity.__str__()
        print self.Abstracted
            
                
    def getjsonGlobalIndex(self):
        filename = const.SAVING_ROUTE + '/index.json'
        
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
        else:
            print "filenotfound "+filename
            
    def notbeenfound(self):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json' 
        jOmNews = { 
           "title": const.DELIVERY_DESCRIPTION_PRINTED,
           "publication": const.PUB_NAME,
           "company": const.COMPANY_NAME,
           "message": "No se ha encontrado la fecha seleccionada",
           "debug": filename,
           "status" : "noresults"
           }  
        self.result = json.dumps(jOmNews)
    
    def actionresponse(self, action, param, status):        
        jOmNews = { 
           "title": const.DELIVERY_DESCRIPTION_UPDATES,
           "publication": const.PUB_NAME,
           "company": const.COMPANY_NAME,
           "message": "action=" + action + "; param=" + param,
           "status" : status
           }
        self.result =  json.dumps(jOmNews)
        
    def runrequest(self):
        mjson = json.loads(self.json,'utf-8')
        content = mjson['content']

        for k,v in content.items():
                for k2, v2 in v.items():
                    for k3,v3 in v2.items():
                        if v3:
                            for k4,v4 in v3.items():
                                if v4:
                                    c = len(self.rWords)
                                    f = 0
                                    for rword in self.rWords:
                                        if rword in v4:
                                            f += 1
                                            print "found "+rword+ " at " + k + "/" + k2 + "/" + k3 + "/" + k4
                                            print "rel " + str(f)

            
    
    def dispatchRichness(self, jItem):
        if isinstance(jItem, dict):
            level = self.richness
            if level == 'all':
                return jItem
            else:
                nItem = jItem[level]
                return nItem     
        return jItem
        
            
    def getResult(self):
        return self.result  

                      
if __name__ == '__main__':
    miapi =Search(txt="El Palacio de Hierro")
    #print miapi.getResult()
    
    
            
            

 

     
        
        