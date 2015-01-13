# -*- coding: utf-8 -*-


import sys, os
from compiler.ast import TryExcept

path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))

import logging
import httplib
import json
import constants as const
from datetime import datetime
import time
import urllib


SERVER = 'cp.pushwoosh.com'
BASEURL = "https://cp.pushwoosh.com/json/1.3/"

class Updater(object):
    
    MAX_SIM_PUSH = 1

    def __init__(self): 
        logging.getLogger().setLevel(logging.INFO)
        self.updates = []      
        self.current = ""
        self.prev = ""
        self.result = ""             
        self.getjson()

        if len(self.current)>1:
            if len(self.prev)>1:
                self.runrequest()
        else: 
            pass
            self.notbeenfound()
                
    def getjson(self):
        current = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'last.json'
        prev = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'prev.json'
            
        if os.path.isfile(current):
            f = open(current, 'r')
            self.current = f.read()
            f.close()
        else:
            logging.debug("filenotfound "+ current)
            
            
        if os.path.isfile(prev):
            logging.info("getting file: " + prev)
            f = open(prev, 'r')
            self.prev = f.read()
            f.close()
        else:
            logging.debug("filenotfound "+ prev)
            
    def getPushCurrentHistory(self):
        path = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'current_history.json'             
        if os.path.isfile(path):
            f = open(path, 'r')
            jsontxt = f.read()
            f.close()
            try:
                return json.loads(jsontxt,'utf-8')
            except:
                logging.debug("history json error"+ path)
        else:
            logging.debug("history filenotfound "+ path)
            return
            
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
        foundnew = False
        didpush = 0
        
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
                logging.info("new Note: " + currId)
                del thisNote['content']
                
                #ADD NOTE  IF RELEVANT
                if (thisNote['type']!='foto'):
                    if (thisNote['family']=='uportada'):
                        foundnew = True
                        if (didpush<self.MAX_SIM_PUSH):
                            self.updates.append(thisNote['title'] )
                            logging.info("pushing " + thisNote['title'])
                            self.pushThisNote(thisNote['title'], thisNote['navUrl'], thisNote['id'])
                            didpush += 1
                        else:
                            logging.info("max sim reached ")
                    else:
                        logging.info("not portada")
                else:
                    logging.info("is foto")
                
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
            
        if (foundnew) :
            logging.info("new content found and pushed")
        else:
            logging.info("no new content")

    def checkAlreadyPushed(self, noteid):
        history = self.getPushCurrentHistory()
        if (history is not None):
            for item in history:
                logging.info("->noteid  %s" % item["noteid"])
                try:
                    if (item["noteid"] == noteid):
                        logging.info("->already pushed %s" % noteid)
                        return True
                except:
                    logging.info("error checking if sent, assuming is not yet pushed")
                    return False
        else:
            return False
        
    def purgePushHistory(self):
        history = self.getPushCurrentHistory()
        if (history is not None):
            for item in history:
                logging.info("->note time  %s" % item["time"])
                try:
                    timeis = datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S.%f" )
                    now = datetime.now()
                    logging.info(timeis)
                    logging.info(now)
                    delta = (now - timeis).total_seconds()
                    logging.info(delta)
                except:
                    logging.info("error PURGE")
                    return False
        else:
            return False
    
    def registerPushed(self, text, link, noteid, request):
        logging.info("saving push to log...")
        path_curr = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'current_history.json'
        now = datetime.now()
        push = {
            "text":text,
            "link":link,
            "noteid":noteid,
            "time": str(now),
            "timestamp": now.microsecond,
            "request": request
        }
        history = self.getPushCurrentHistory()
        if (history is not None):
            history.append(push)
            self.saveJSON(history, path_curr)
        else:
            history = []
            history.append(push)
            self.saveJSON(history, path_curr)
    
    def saveJSON(self, text, pathname):
        j =  json.dumps(text, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        f = open(pathname, 'w')
        f.write(j)
        f.close()
        
    def pushThisNote(self, text, link, noteid):
        if self.checkAlreadyPushed(noteid):
            logging.info("skipping already pushed")
            return
        appcode = "EA506-AAE0E"
        #appcode = "27D11-8F224" #debugging appcode
        token = "5y2m8EkDJ1urdRPQfIFYpQguNhxXqBk/nvyx7vKnANrUpsseqvN6VmiNJuUPfosXrcE0BWpORQlK9/c9nvgY"
        url = BASEURL + 'createMessage'
        request = {
            "request":{
                "application":appcode,
                "auth":token,
                "notifications":[
                   {
                      "send_date":"now", 
                      "ignore_user_timezone": True,
                      "content": text,
                      "data": {
                            "noteid": noteid
                      },     
                   }
                ]
            }
        }
        body = json.dumps(request)
        logging.info(body)
        code, response = self._request("POST", body, url)
        logging.info(response)
        
        if code != 200:
            logging.error("error code->")
            logging.error(code)
        else:
            dresponse = json.loads(response)
            status = dresponse['status_code']
            response = dresponse['status_message']
            logging.info(status)
            logging.info(response)
            self.registerPushed(text, link, noteid, request)
    
    def _request(self, method, body, url):
        connection = httplib.HTTPSConnection(SERVER)
        headers = {'content-type': 'application/json'}
        connection.request(method, url, body=body, headers=headers)
        resp = connection.getresponse()
        return resp.status, resp.read()
        
            
    def getResult(self):
        return self.result
    
    def getMicroID(self, _id):
        _id = _id.replace("http://www.jornada.unam.mx/ultimas/","")
        _id = _id.replace(".html","")
        _id = _id.replace("/","-")
        _id = _id[11:]
        _id = _id[:60]
        return _id
    
    def getMicroURL(self, url):
        logging.info( url )
        url = urllib.quote(url, '')
        logging.info( url )
        host = 'api-ssl.bitly.com'
        param = '/v3/shorten?access_token=e46f80c6ed667c062da9fefc2fe410360cb9acd0&longUrl=' + url
        conn = httplib.HTTPSConnection(host)
        logging.info( host+param )
        conn.request("GET", param)
        r1 = conn.getresponse()
        logging.info(r1.status)
        logging.info(r1.reason)
        newurl = url
        response = r1.read()
        try:
            data = json.loads(response)
            newurl = data['data']['url']
            logging.info( 'shorten' )
        except:
            logging.info( 'no shorten' )
            pass
        logging.info( newurl )
        return newurl

                      
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("update detection finished")
    updater = Updater()
    #text = u"Reinician en el Senado negociación sobre reforma político-electoral"
    #link = ""
    #noteid = "reinician-en-el-senado-negociacion-de-leyes-reglamentarias-e"
    #updater.pushThisNote(text, link, noteid)
    #updater.purgePushHistory()
    
    
 

     
        
        
