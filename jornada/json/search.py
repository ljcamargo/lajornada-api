# -*- coding: utf-8 -*-

import json
import os
from linguistics.gramatics.esp import ESP as LANG
from linguistics.gramatics.heuristics import Heuristics
from datetime import datetime as dayt
from datetime import timedelta
from operator import itemgetter
import constants as const
from collections import defaultdict
from pymongo import Connection


class Search(object):

    def __init__(self, txt="", richness="html", source="impresa", detail="full"):
        self.DETAIL_NO_CONTENT = "nocontent"
        self.DETAIL_MINIMAL = "minimal"
        self.txt = txt if txt != None else ""
        self.richness = richness if (richness != None or richness == "") else "html"
        self.source = source if source != None else "impresa"
        self.detail = detail if detail != None else "full"
        self.json = "" 
        self.html = ""
        self.result = ""
        self.resultItems = []
        self.rWords = []
        self.rOddity = defaultdict(int)
        self.Abstracted = ""
          
        if not self.richness in ['html','plain','list','all']:
            self.richness = 'html'

        if not self.detail in ['nocontent','minimal','full']:
            self.detail = 'nocontent'
            
            
        #MONGO DB CONN
        self.connection = Connection('localhost')
        self.db = self.connection.lajornada
        self.collection = self.db.lajornada_notas
        self.index = self.db.lajornada_index
            
        self.preProcessSearchString(self.txt)                 
        self.searchInDB()
        self.genJson()
                
        
    def preProcessSearchString(self, text):
        heur = Heuristics('esp')
        abstr = []
        heur._matchTextToList(text, self.rWords)
        heur._proccessOddness(text, self.rOddity)
        heur._processAbstraction(text, abstr)
        self.rWords = heur.makeKeywordAbstractList(self.rWords)
        self.Abstracted = "".join(abstr)
        print "words" + self.rWords.__str__()
        print self.rOddity.__str__()
        print self.Abstracted
            
                
    def searchInDB(self):
        print "collection has " + str(self.collection.count())
        for item in self.index.find({"keywords":{"$all":self.rWords}}).sort("timestamp",-1).limit(12):
            print item['timestamp']
            print item['id']
            print item['keywords']
            jItem = {
                     "id": item['id'],
                     "timestamp": item['timestamp'],
                     "keywords": item['keywords']
            }  
            
            
            for iitem in self.collection.find(   { "$and": [ {  "timestamp":item['timestamp']  }  ,  { "id":item['id'] }   ]}  ):
                print iitem['timestamp']
                print iitem['id']
                print iitem['keywords']
                jItem2 = {
                     "id": iitem['id'],
                     "year": iitem['year'],
                     "month": iitem['month'],
                     "day": iitem['day'],
                     "timestamp":iitem['timestamp'],
                     "index":iitem['index'],
                     "page":iitem['page'],
                     "order":iitem['order'],
                     "family": iitem['family'],
                     "section": iitem['section'],
                     "type": iitem['type'],
                     "noteXmlUrl": iitem['noteXmlUrl'],
                     "navUrl": iitem['navUrl'],
                     "title": iitem['title'],
                     "edTitle": iitem['edTitle'],
                     "summary": iitem['summary'],
                     "edSummary": iitem['edSummary'],
                     "abstract": iitem['abstract'],
                     "series": iitem['series'],
                     "author": iitem['author'],
                     "date": iitem['date'],
                     "audio":iitem['audio'],
                     "images": iitem['images'],
                     "content": iitem['content'],
                     "keywords": iitem['keywords']
                }
                self.resultItems.append(jItem2)
            
            

    def genJson(self):
        jOmNews = { 
           "title": const.DELIVERY_DESCRIPTION_PRINTED,
           "publication": const.PUB_NAME,
           "isbn": const.PUB_ISBN,
           "periodicity": const.PUB_PERIODICITY_PRINTED,
           "gentime": const.PUB_GENTIME_PRINTED,
           "timezone": const.LOCALE_TIMEZONE,
           "company": const.COMPANY_NAME,
           "country": const.LOCALE_COUNTRY,
           "region": const.LOCALE_REGION,
           "language":const.LOCALE_LANG,
           "culture":const.LOCALE_CULTURE,
           "encoding":const.LOCALE_ENCODING,
           "webpage": const.PUB_WEB,
           "scope" : const.PUB_SCOPE,
           "alias": const.DELIVERY_ALIAS_PRINTED, 
           "contentKind": const.DELIVERY_KIND_PRINTED,
           "query": self.txt,
           "results_count": self.resultItems.__len__(),
           "content": self.resultItems,
           }
        self.json = jOmNews
                              
            
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
            
    
    def dispatchRichness(self, jItem):
        if isinstance(jItem, dict):
            level = self.richness
            if level == 'all':
                return jItem
            else:
                nItem = jItem[level]
                return nItem     
        return jItem
        
            
    def getHTML(self):
        mjson = self.json
        precontent =  mjson["content"]
        html_head = "<html><header><title>Resultados</title></head>"
        html_head += '<link rel="stylesheet" href="cloud.css"/>'
        html_body = "<body>"
        html_content = '<div class="item_block">Resultados para:<h3>'+self.txt+'</h3></div><br>'
        html_end = "</body></html>"
        for c in xrange(len(precontent)-1,-1,-1):
            thisNote = precontent[c]
            if thisNote.get('content'):
                #thisNote['summary']=self.dispatchRichness(thisNote['summary'])
                html_content += '<div class="item_result"><a href="'+thisNote['navUrl']+'">'
                html_content += "<h3>"+self.highlightSearchItem(thisNote['title'])+"</a></h3>"
                html_content += "<p><b>"+thisNote['day']+"/"+thisNote['month']+"/"+thisNote['year']+"</b></p>"
                html_content += "<p><small>"+self.highlightSearchItem(thisNote['summary']['plain'])+"</small></p>"
                for image in thisNote.get('images'):
                    html_content += '<div class="item_image"><img src="'+image['snap']+'"></img><p><small>'+image['caption']+'</small></p></div>'
                html_content += "</div>"                   
        self.html = html_head+html_body+html_content+html_end
        filename = const.SAVING_ROUTE + '/query_search.html'
        f = open(filename, 'w')
        print 'writting file: %s' % filename
        f.write(self.html)
        f.close()
        self.result = self.html
        
    def highlightSearchItem(self, text):
        for word in self.txt.split():
            text = text.replace(word,'<b>'+word+'</b>')
        return text
        
    def getResult(self):
        mjson = self.json
        precontent =  mjson["content"]
        newcontent = []
        for c in xrange(len(precontent)-1,-1,-1):
            thisNote = precontent[c]
            include = True
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
                    if self.detail == self.DETAIL_NO_CONTENT:
                        del thisNote['content']
                    if self.detail == self.DETAIL_MINIMAL:
                        del thisNote['content']
                        del thisNote['summary']
                        del thisNote['edSummary']
                        del thisNote['abstract']
                        
                newcontent.append(thisNote)
        self.result =  json.dumps(mjson, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        print "result"
        #print self.result
        filename = const.SAVING_ROUTE + '/query_search.json'
        f = open(filename, 'w')
        print 'writting file: %s' % filename
        f.write(self.result)
        f.close()
                      
if __name__ == '__main__':
    miapi =Search(txt=u"15 de Septiembre")
    #print miapi.getResult()
    miapi.getHTML()
    
    
            
            

 

     
        
        