# -*- coding: utf-8 -*-


import sys, os
path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))
import json
import constants as const
from jornada.push.notifications import NotificationsManager
from datetime import datetime



class Updater(object):

    def __init__(self): 
        self.updates = []      
        self.current = ""
        self.prev = ""
        self.result = ""             
        self.getjson()
        
        if len(self.current)>1:
            if len(self.prev)>1:
                self.runrequest()
        else: 
            self.notbeenfound()
                
    def getjson(self):
        current = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'last.json'
        prev = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'prev.json'
            
        if os.path.isfile(current):
            #print "getting file: " + current
            f = open(current, 'r')
            self.current = f.read()
            f.close()
        else:
            print "filenotfound "+ current
            
            
        if os.path.isfile(prev):
            print "getting file: " + prev
            f = open(prev, 'r')
            self.prev = f.read()
            f.close()
        else:
            print "filenotfound "+ prev
            
    def notbeenfound(self):
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
        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        mjson = json.loads(self.current,'utf-8')
        postcontent =  mjson[0]["content"]
        pjson = json.loads(self.prev,'utf-8')
        precontent =  pjson[0]["content"]
        newcontent = []
        
        for c in xrange(len(postcontent)-1,-1,-1):
            thisNote = postcontent[c]
            currId = thisNote.get('id')
            isPresent = False
            for d in xrange(len(precontent)-1,-1,-1):
                preNote = precontent[d]
                prevId = preNote.get('id')
                if prevId == currId:
                    isPresent = True
            if not isPresent:
                del thisNote['content']
                del thisNote['summary']
                del thisNote['edSummary']
                del thisNote['abstract']  
                del thisNote['images']   
                del thisNote['audio'] 
                del thisNote['order']
                del thisNote['page']
                del thisNote['series'] 
                
                #ADD NOTE  
                self.updates.append(thisNote['title'] )
                #/ADD NOTE
                    
                newcontent.append(thisNote)
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION_UPDATES,
               "publication": const.PUB_NAME,
               "isbn": const.PUB_ISBN,
               "periodicity": const.PUB_PERIODICITY_CURRENT,
               "gentime": const.PUB_GENTIME_CURRENT,
               "timezone": const.LOCALE_TIMEZONE,
               "company": const.COMPANY_NAME,
               "country": const.LOCALE_COUNTRY,
               "region": const.LOCALE_REGION,
               "language":const.LOCALE_LANG,
               "culture":const.LOCALE_CULTURE,
               "encoding":const.LOCALE_ENCODING,
               "webpage": const.PUB_WEB,
               "date": date,
               "scope" : const.PUB_SCOPE,
               "alias": const.DELIVERY_ALIAS_UPDATES, 
               "contentKind": const.DELIVERY_KIND_UPDATES,
               "status" : "success",   
               "content": newcontent,
               }
        self.result =  json.dumps(jOmNews)
        #self.pushUpdates()
    
    def pushUpdates(self):
        pushtxt = ';'.join(self.updates)
        push = NotificationsManager()
        #print pushtxt
        push.sendPushToUserList("default", pushtxt, "La Jornada")
        
            
    def getResult(self):
        return self.result  

                      
if __name__ == '__main__':
    miapi =Updater()
    print "done"

 

     
        
        