# -*- coding: utf-8 -*-


import sys, os

path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))

import logging
import httplib
import json
import constants as const
from datetime import datetime
import urllib


SERVER = 'cp.pushwoosh.com'
BASEURL = "https://cp.pushwoosh.com/json/1.3/"

class Updater(object):
    
    MAX_SIM_PUSH = 3

    def __init__(self): 
        logging.getLogger().setLevel(logging.INFO)
        self.updates = []      
        self.current = ""
        self.prev = ""
        self.result = ""             
        self.getjson()

        if len(self.current)>1:
            if len(self.prev)>1:
                pass
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
                del thisNote['content']
                
                #ADD NOTE  IF RELEVANT
                if (thisNote['type']!='foto'):      
                    if (thisNote['family']=='uportada'):
                        if (thisNote['order']<3):               
                            foundnew = True
                            if (didpush<self.MAX_SIM_PUSH):
                                self.updates.append(thisNote['title'] )
                                #logging.info("pushing %" % thisNote['title'])
                                self.pushThisNote(thisNote['title'], thisNote['navUrl'], thisNote['id'])
                                didpush += 1       
                
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

        
    def pushThisNote(self, text, link, noteid):
        noteid = self.getMicroURL(noteid)
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
    
    def _request(self, method, body, url):
        """ private request function """
        connection = httplib.HTTPSConnection(SERVER)
        headers = {'content-type': 'application/json'}
        connection.request(method, url, body=body, headers=headers)
        resp = connection.getresponse()
        return resp.status, resp.read()
        
            
    def getResult(self):
        return self.result
    
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
    updater =Updater()
    #text = u"Inicia pleno del Senado discusión de la reforma energética "
    #link = ""
    #noteid = "http://www.jornada.unam.mx/ultimas/2013/12/10/inicia-pleno-del-senado-discusion-de-la-reforma-energetica-7051.html"
    #updater.pushThisNote(text, link, noteid)
    
    
 

     
        
        
