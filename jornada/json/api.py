# -*- coding: utf-8 -*-

import json
import os
from impresa import Impresa
from datetime import datetime as dayt
from datetime import timedelta
from multiprocessing import Pool
import constants as const




class Api(object):

    def __init__(self, family="", section="", mtype="", txt="", noteid="", year="", month="", day="", detail="", richness="html", source="impresa"):
        self.DETAIL_NO_CONTENT = "nocontent"
        self.DETAIL_MINIMAL = "minimal"
        self.family = family if family != None else ""
        self.section = section if section != None else ""
        self.type = mtype if mtype != None else ""
        self.txt = txt if txt != None else ""
        self.noteid = noteid if noteid != None else ""
        self.year = year if year != None else ""
        self.month = month if month != None else ""
        self.day = day if day != None else ""
        self.detail = detail if detail != None else ""
        self.richness = richness if (richness != None or richness == "") else "html"
        self.source = source if source != None else "impresa"
        self.json = "" 
        self.result = ""
        
        if not self.richness in ['html','plain','list','all']:
            self.richness = 'html'

        if not self.detail in ['nocontent','minimal','full']:
            self.detail = 'full'
            
        if not self.source in ['impresa','ultimas']:
            self.detail = 'impresa'
                  
        if self.year=="" or self.month=="" or self.day=="":
            self.getDate()
                        
        self.getjson()
        
        if len(self.json)>1:
            self.runrequest()
        elif self.source == "ultimas":
            self.getpastjson()
            if len(self.json)>1:
                self.runrequest()
            else:
                self.notbeenfound()
        else: 
            self.getPastDate()
            self.getjson()
            if len(self.json)>1:
                self.runrequest()
            else:
                self.notbeenfound()
        
    def getDate(self):
        now = dayt.now()
        self.year = str(now.year)
        self.month = str(now.month)
        if len(self.month) < 2:
            self.month = "0"+self.month     
        self.day = str(now.day)
        if len(self.day) < 2:
            self.day = "0"+self.day 
            
    def getPastDate(self):
        print ('past date')
        now = dayt.now()-timedelta(days=1)
        self.year = str(now.year)
        self.month = str(now.month)
        if len(self.month) < 2:
            self.month = "0"+self.month
        self.day = str(now.day)     
        if len(self.day) < 2:
            self.day = "0"+self.day
            
    def asyncInvokeDailyFileGeneration(self):
        pool = Pool(processes=1)
        pool.apply_async(Impresa(), [], None) 
                
    def getjson(self):
        if self.source == "impresa":
            if len(self.month) < 2:
                self.month = "0"+self.month     
            if len(self.day) < 2:
                self.day = "0"+self.day 
            filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json'
        else:
            filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'last.json'
            
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
        else:
            print "filenotfound "+filename
            
    def getpastjson(self):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'prev.json'
            
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
        else:
            print "filenotfound "+filename
            
    def notbeenfound(self):
        if self.source == "impresa":
            filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json' 
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION_PRINTED,
               "publication": const.PUB_NAME,
               "company": const.COMPANY_NAME,
               "message": "No se ha encontrado la fecha seleccionada",
               "debug": filename,
               "status" : "noresults"
               }
        else:
            filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'last.json'
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION_CURRENT,
               "publication": const.PUB_NAME,
               "company": const.COMPANY_NAME,
               "message": "No se ha encontrado el recurso seleccionada",
               "debug": filename,
               "status" : "noresults"
               }
        
        self.result = json.dumps(jOmNews)
        
    def requesterror(self, error):        
        if self.source == "impresa":
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION_PRINTED,
               "publication": const.PUB_NAME,
               "company": const.COMPANY_NAME,
               "message": "Ha ocurrido un error en la petición: ",
               "debug": error,
               "status" : "error"
               }
        else:
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION_CURRENT,
               "publication": const.PUB_NAME,
               "company": const.COMPANY_NAME,
               "message": "Ha ocurrido un error en la petición: ",
               "debug": error,
               "status" : "error"
               }
        
        self.result =  json.dumps(jOmNews)  
        
    def runrequest(self):
        try:
            mjson = json.loads(self.json,'utf-8')
            precontent =  mjson[0]["content"]
            newcontent = []
            for c in xrange(len(precontent)-1,-1,-1):
                thisNote = precontent[c]
                include = True
                if self.family != "":
                    if thisNote.get('family') != self.family:
                        include = False
                if self.type != "":
                    if thisNote.get('type') != self.type:
                        include = False
                if self.section != "":
                    if thisNote.get('section') != self.section:
                        include = False
                if self.noteid != "":
                    if thisNote.get('id') != self.noteid:
                        include = False
                if self.txt != "":
                    if thisNote.get('title').find(self.txt) == -1:
                        include = False
                if include:        
                    #edit note
                    #dispatch richness
                    if thisNote.get('content'):
                        thisNote['summary']=self.dispatchRichness(thisNote['summary'])
                        thisNote['edSummary']=self.dispatchRichness(thisNote['edSummary'])
                        thisNote['content']['title']=self.dispatchRichness(thisNote['content']['title'])
                        thisNote['content']['hedline']=self.dispatchRichness(thisNote['content']['hedline'])
                        thisNote['content']['abstract']=self.dispatchRichness(thisNote['content']['abstract'])
                        thisNote['content']['text']=self.dispatchRichness(thisNote['content']['text'])
                        
                        #dispatch detail
                        if self.detail != ("" or "full"):
                            if self.detail == self.DETAIL_NO_CONTENT:
                                del thisNote['content']
                            if self.detail == self.DETAIL_MINIMAL:
                                del thisNote['content']
                                del thisNote['summary']
                                del thisNote['edSummary']
                                del thisNote['abstract']
                    newcontent.append(thisNote)
            mjson[0]["content"] = newcontent
            self.result =  json.dumps(mjson)
        except Exception as e:
            self.requesterror(e.__str__())
    
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
    miapi =Api("","","","","","","","","full","plain")
    print miapi.getResult()
    
    
            
            

 

     
        
        