# -*- coding: utf-8 -*-
'''
Created on 13/05/2012

@author: lcammx
'''
import sys, os
path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))

from collections import defaultdict
from xml.dom import minidom
import json
import constants as const
from operator import itemgetter
from linguistics.gramatics.esp import ESP
from linguistics.gramatics.heuristics import Heuristics
from datetime import timedelta, datetime
import datetime as datetime2
import time
from feedparser import FeedParser
#from pymongo import Connection

class Impresa(FeedParser):
    
    def __init__(self, minus=0, day=0, month=0, year=0):
        if (day!=0 and month!=0 or year!=0):
            now = datetime2.date(year, month, day)  
        elif minus!=0:
            now = datetime.now()-timedelta(days=minus)   
        else:
            now = datetime.now()  
        status="success"
        self.server = "unam"
        self.year = str(now.year)
        self.month = str(now.month)
        if len(self.month) < 2:
            self.month = "0"+self.month     
        self.day = str(now.day)
        if len(self.day) < 2:
            self.day = "0"+self.day   
        self.imgSize = const.CONFIG_IMGSIZE
        self.snapSize = const.CONFIG_SNAPSIZE
        self.superfamily = "portada"
        
        #MONGO DB CONN
        #self.connection = Connection('localhost')
        #self.db = self.connection.lajornada
        #self.collection = self.db.lajornada_notas
        #self.index = self.db.lajornada_index
        #self.collection.drop()
        #self.index.drop()
        #return

        jItems = []
        self.Entropy = defaultdict(int)
        self.Keywords = defaultdict(int)
        self.jAnalytics = []
        self.jHeuristics = []
        self.jAbstracted = ""
        self.jMaster = defaultdict(int)
        self.lang = ESP()
        self.heur = Heuristics("es")
        
        jItems = self.getNoteItemsFromDir(jItems)
        jItems = self.getNoteItemsFromPortada(jItems)
        jItems = self.getNoteItemsFromContra(jItems)
        jItems = self.getNoteItemsFromCartones(jItems)
        jItems = self.getNoteItemsFromAudioN(jItems)
    
        date = "" + str(self.year) + "/" + str(self.month) + "/" + str(self.day)
        orderedItems = sorted(jItems, key=itemgetter('index'))
        #VOLCATE TO MONGODB;
        #for item in jItems:
            #self.genNodeForDB(item)
            
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
           "date": date,
           "scope" : const.PUB_SCOPE,
           "alias": const.DELIVERY_ALIAS_PRINTED, 
           "contentKind": const.DELIVERY_KIND_PRINTED,
           "status" : status,   
           "content": orderedItems,
           }
        self.dumpJsonItems([jOmNews])
        
        lang = ESP()
        self.heur = Heuristics("es")
        for k,v in self.jMaster.iteritems():
            if lang.wordOddnessScore(k)>2:
                k = self.heur.stripWordEnclousureMarks(k)
                self.Entropy[k]= v
        
        try:            
            self.jAnalytics = { 
                    "title": "impresa",
                    "date": date,
                    "incidence" : self.jMaster,
                    "oddity" : self.Entropy,
                    "keywords": self.Keywords,
                    "content" : self.jHeuristics,
                    "abstracted" : self.jAbstracted
                    }
            #self.dumpJsonHeuristics(self.jAnalytics)
        except Exception as error2:
            self.dumpErrorLog(error2)
        
            
    ''' DB SUPPORT
    def upsertNoteToDB(self, Note, index):
        print "upsert mongo "+Note['id']+"  keyw:"+'|'.join(Note['keywords'])
        self.collection.update({'id':Note['id'], 'year':self.year,'month':self.month,'day':self.day}, Note, upsert=True)
        self.index.update({'id':index['id'], 'timestamp':index['timestamp']}, index, upsert=True)
        print "collection has now" + str(self.collection.count())
    '''    
            
    def dumpJsonItems(self, jItems):
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json'
        f = open(filename, 'w')
        print 'Escribiendo archivo: %s' % filename
        f.write(j)
        f.close()
        
    def dumpJsonHeuristics(self, jItems):
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def dumpErrorLog(self, error):
        now = datetime.now()
        jError = [{ 
           "title": u"Log Errores Noticias Impresas Periódico La Jornada",
           "publication": u"La Jornada",
           "time": now.strftime("%Y-%m-%d %H:%M:%S"),
           "alias": "error_log_lajornada_impresa", 
           "message" : error.__str__()
           }]
        j =  json.dumps(jError, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=True)
        filename = const.SAVING_ROUTE + "/" + const.SAVING_ERROR_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '_' + now.strftime("%H_%M_%S") + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
        
    ''' DB SUPPORT     
    def genNodeForDB(self, MongojItem):
        MongojItem['year']=self.year
        MongojItem['month']=self.month
        MongojItem['day']=self.day
        dt0 = datetime(year=2000, month=1, day=1)
        timestamp = time.mktime(dt0.timetuple())
        dt = datetime(year=int(self.year), month=int(self.month), day=int(self.day))
        timestamp = time.mktime(dt.timetuple()) - timestamp
        MongojItem['timestamp']=timestamp
        heur = Heuristics('esp')
        MongojItem['keywords']=heur.makeKeywordAbstractList(MongojItem['keywords'])
        MongoIndex = {
                      "id":MongojItem['id'],
                      "timestamp":MongojItem['timestamp'],
                      "keywords":MongojItem['keywords']
        }
        self.upsertNoteToDB(MongojItem,MongoIndex)
    '''
        
    def getNoteItemsFromDir(self, jItems):
        family = "dir"
        filestr = self.getHttpResourceString('dir')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            navUrl = self.getNavUrl(nodeid)
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            page = self.getRecursiveText(node.getElementsByTagName('page'))
            order = self.getRecursiveText(node.getElementsByTagName('ord'))
            
            page = self.getIntFromText(page)
            order = self.getIntFromText(order)
            
            title = self.getRecursiveText(node.getElementsByTagName('title'))

            firstplst = node.getElementsByTagName('firstp')
            summary = {
                "html" :  self.getHtmlFromParragraphs(firstplst),
                "plain" : self.getRecursiveText(firstplst),
                "list" : self.getListItems(firstplst)
            }
            
            series = self.getRecursiveText(node.getElementsByTagName('series'))       
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('date'))           
            
            abstractlst = xmldoc.getElementsByTagName('abstract')[0].childNodes
            abstract = {
                "html" :  self.getHtmlFromParragraphs(abstractlst),
                "plain" : self.getRecursiveText(abstractlst),
                "list" : self.getListItems(abstractlst)
            }
            
            medialst = node.getElementsByTagName('media')
            imgs = self.getImagesObject(medialst)
                
            #EACH NOTE PARSING
            notecontent = self.getNoteContent(nodeid)
            
            keywords = notecontent['keywords']
            del notecontent['keywords']
                        
                        
            jItem = {
                     "id": nodeid,
                     "index":(page*order),
                     "page":page,
                     "order":order,
                     "family": family,
                     "section": section,
                     "type": type,
                     "noteXmlUrl": noteXmlUrl,
                     "navUrl": navUrl,
                     "title": title,
                     "edTitle": title,
                     "summary": summary,
                     "edSummary": summary,
                     "abstract": "",
                     "series": series,
                     "author": author,
                     "date": date,
                     "audio":"",
                     "images": imgs,
                     "content": notecontent,
                     "keywords": keywords
            }   
            
            jItems.append(jItem)
    
        #RAYUELA
        rayuela = xmldoc.getElementsByTagName('Rayuela')[0]
        section = "rayuela"
        type = "bullet"
        title = self.getRecursiveText(rayuela)
        abstract = ""    
        raykw = []
        self.heur._matchTextToList(title, raykw)
        raykw.append('@rayuela')
        rayid = 'ray01'
        new = {
             "id": "",
             "index":rayid,
             "page": 0,
             "order": 0,
             "family": "contra",
             "section": "rayuela",
             "type": type,
             "noteXmlUrl": "",
             "navUrl": "",
             "title": title,
             "edTitle": title,
             "summary": [],
             "edSummary": [],
             "abstract": "",
             "series": "",
             "author": "",
             "date": "",
             "audio":"",
             "images": [],
             "content": [],
             "keywords": raykw
        }
        
        jItems.append(new)
        jItems= sorted(jItems,  key=lambda k: k['order'])   
        return jItems
    
    
        
    def getNoteItemsFromPortada(self, jItems):
        family = "portada"
        filestr = self.getHttpResourceString('portada')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            navUrl = self.getNavUrl(nodeid)
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            title = self.getRecursiveText(node.getElementsByTagName('title'))
            firstplst = node.getElementsByTagName('firstp')
            summary = {
                "html" :  self.getHtmlFromParragraphs(firstplst),
                "plain" : self.getRecursiveText(firstplst),
                "list" : self.getListItems(firstplst)
            }      
            series = self.getRecursiveText(node.getElementsByTagName('series'))       
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('date'))

            abstractlst = node.getElementsByTagName('abstract')
            abstract = self.getArray(abstractlst)
            
            medialst = node.getElementsByTagName('media')
            imgs = self.getImagesObject(medialst)
                      
            for i in xrange(len(jItems)-1,-1,-1):
                if jItems[i].get('id') == nodeid:
                    preimgs = jItems[i].get('images')
                    if len(preimgs)>0:
                        for ii in xrange(len(preimgs)-1,-1,-1):
                            for iii in xrange(len(imgs)-1,-1,-1):
                                if preimgs[ii].get('id') == imgs[iii].get('id'):
                                    preimgs[ii] = imgs[iii]
                                else:
                                    preimgs.append(imgs[iii])

                    else:
                        preimgs = imgs
                    new = {
                         "id": nodeid,
                         "index":jItems[i].get('index'),
                         "page": jItems[i].get('page'),
                         "order": jItems[i].get('order'),
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
                         "navUrl": navUrl,
                         "title": jItems[i].get('title'),
                         "edTitle": title,
                         "summary": jItems[i].get('summary'),
                         "edSummary": summary,
                         "abstract": abstract,
                         "series": series,
                         "author": author,
                         "date": date,
                         "audio":"",
                         "images": preimgs,
                         "content": jItems[i].get('content'),
                         "keywords": jItems[i].get('keywords') 
                    }
                    jItems[i] = new
                    x += 1

        orphanpics = xmldoc.getElementsByTagName('foto')
        y = 0
        for node in orphanpics:
            nodeid = "foto"+str(y)
            noteXmlUrl =  ""
            section = ""
            stype = "foto"
            title = node.getAttribute('cabeza')
            summary = []
            series = ""
            author = ""
            date = ""
            imgs = []
            url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
            ikind = "main"
            url = self.getImgUrl(node.getAttribute('src'))
            snap = self.getSnapUrl(node.getAttribute('src'))
            keywords = []
            self.heur._matchTextToList(caption, keywords)
            self.heur._matchTextToList(header, keywords)
            img = {
                   "id":node.getAttribute('src'),
                   "url":url,
                   "snap":snap,
                   "alt":node.getAttribute('cabeza'),
                   "caption":node.getAttribute('pie'),
                   "header":node.getAttribute('cabeza'),
                   "author":"",
                   "kind":ikind
                   }
            imgs.append(img)
            abstract = ""    
            new = {
                 "id": nodeid,
                 "index":y,
                 "page": 0,
                 "order": y,
                 "family": family,
                 "section": section,
                 "type": stype,
                 "noteXmlUrl": noteXmlUrl,
                 "navUrl": "",
                 "title": title,
                 "edTitle": title,
                 "summary": summary,
                 "edSummary": summary,
                 "abstract": abstract,
                 "series": series,
                 "author": author,
                 "date": date,
                 "audio":"",
                 "images": imgs,
                 "content": [],
                 "keywords": keywords
            }
            jItems.append(new)
            y += 1
                                              
        jItems= sorted(jItems,  key=lambda k: k['order'])              
        return jItems
    
    def getNoteItemsFromContra(self, jItems):
        family = "contra"
        filestr = self.getHttpResourceString('contra')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 1;
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            navUrl = self.getNavUrl(nodeid)
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            title = self.getRecursiveText(node.getElementsByTagName('title'))
            firstplst = node.getElementsByTagName('firstp')
            summary = {
                "html" :  self.getHtmlFromParragraphs(firstplst),
                "plain" : self.getRecursiveText(firstplst),
                "list" : self.getListItems(firstplst)
            }      
            series = self.getRecursiveText(node.getElementsByTagName('series'))       
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('date'))
            
            abstractlst = node.getElementsByTagName('abstract')
            abstract = self.getArray(abstractlst)
            
            medialst = node.getElementsByTagName('media')
            imgs = self.getImagesObject(medialst)
                
            for i in xrange(len(jItems)-1,-1,-1):
                if jItems[i].get('id') == nodeid:
                    preimgs = jItems[i].get('images')
                    if len(preimgs)>0:
                        for ii in xrange(len(preimgs)-1,-1,-1):
                            for iii in xrange(len(imgs)-1,-1,-1):
                                if preimgs[ii].get('id') == imgs[iii].get('id'):
                                    preimgs[ii] = imgs[iii] 
                                else:
                                    preimgs.append(imgs[iii])
                    else:
                        preimgs = imgs
                    new = {
                         "id": nodeid,
                         "index":jItems[i].get('index'),
                         "page": jItems[i].get('page'),
                         "order": jItems[i].get('order'),
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
                         "navUrl": navUrl,
                         "title": jItems[i].get('title'),
                         "edTitle": title,
                         "summary": jItems[i].get('summary'),
                         "edSummary": summary,
                         "abstract": abstract,
                         "series": series,
                         "author": author,
                         "date": date,
                         "audio":"",
                         "images": preimgs,
                         "content": jItems[i].get('content'),
                         "keywords": jItems[i].get('keywords')
                    }
                    jItems[i] = new
                    x += 1 

        orphanpics = xmldoc.getElementsByTagName('foto')
        
        y = 0
        for node in orphanpics:
            nodeid = "foto"+str(y)
            noteXmlUrl =  ""
            section = ""
            stype = "foto"
            title = node.getAttribute('cabeza')
            summary = []
            series = ""
            author = ""
            date = ""
            imgs = []
            url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
            ikind = "main"
            url = self.getImgUrl(node.getAttribute('src'))
            snap = self.getSnapUrl(node.getAttribute('src'))
            keywords = []
            self.heur._matchTextToList(caption, keywords)
            self.heur._matchTextToList(header, keywords)
            img = {
                   "id":node.getAttribute('src'),
                   "url":url,
                   "snap":snap,
                   "alt":node.getAttribute('cabeza'),
                   "caption":node.getAttribute('pie'),
                   "header":node.getAttribute('cabeza'),
                   "author":"",
                   "kind":ikind
                   }
            imgs.append(img)
            abstract = ""    
            new = {
                 "id": nodeid,
                 "index":y,
                 "page": 0,
                 "order": y,
                 "family": family,
                 "section": section,
                 "type": stype,
                 "noteXmlUrl": noteXmlUrl,
                 "navUrl": "",
                 "title": title,
                 "edTitle": title,
                 "summary": summary,
                 "edSummary": summary,
                 "abstract": abstract,
                 "series": series,
                 "author": author,
                 "date": date,
                 "audio":"",
                 "images": imgs,
                 "content": [],
                 "keywords": keywords
            }
            jItems.append(new) 
            y +=1                               
                 
        jItems= sorted(jItems,  key=lambda k: k['order'])        
        return jItems
    
    def getNoteItemsFromCartones(self, jItems):
        family = "cartones"
        filestr = self.getHttpResourceString('cartones')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            noteXmlUrl =  ''
            section = node.getAttribute('cartones')
            type = "foto"

            curl=""
            urllst = node.getElementsByTagName('url')[0].childNodes[0]
            curl = urllst.nodeValue
            
            cthumb=""
            thumblst = node.getElementsByTagName('thumbnail')[0].childNodes[0]   
            cthumb = thumblst.nodeValue
            
            cauthor=""
            authorlst = node.getElementsByTagName('author')[0].childNodes[0]   
            cauthor = authorlst.nodeValue
            
            ccaption=""
            captionlst = node.getElementsByTagName('caption')[0].childNodes[0]   
            ccaption = captionlst.nodeValue
            
            curl = self.getImgOriginalUrl(curl)
            cthumb = self.getImgOriginalUrl(cthumb)
            
            imgs = []
            ikind = "main"
            
            keywords = []
            self.heur._matchTextToList(ccaption, keywords)
            self.heur._matchTextToList(cauthor, keywords)
            keywords.append('@cartones')
            img = {
                       "id":curl,
                       "url":curl,
                       "snap":cthumb,
                       "alt":ccaption,
                       "caption":ccaption,
                       "header":"",
                       "author":cauthor,
                       "kind":ikind
                       }
            imgs.append(img)
            
            jItem = {
                         "id": curl,
                         "index":x,
                         "page": 0,
                         "order": x,
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
                         "navUrl": "",
                         "title": ccaption,
                         "edTitle": ccaption,
                         "summary": cauthor,
                         "edSummary": cauthor,
                         "abstract": "",
                         "series": "",
                         "author": cauthor,
                         "date": "",
                         "audio":"",
                         "images": img,
                         "content": [],
                         "keywords": keywords
                    }              
                            
            jItems.append(jItem)
            x += 1     
        return jItems
    
    def getNoteItemsFromAudioN(self, jItems):
        filestr = self.getHttpResourceString('audion')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('item')
        for node in directory:
            guid=""
            guidlst = node.getElementsByTagName('guid')[0].childNodes[0]
            guid = guidlst.nodeValue
            
            audio=""
            enclosure = node.getElementsByTagName('enclosure')[0]
            audio = enclosure.getAttribute('url')
            
            for items in jItems:
                if items['id']==guid:
                    items['audio']=audio
        return jItems
    
    
               
if __name__ == '__main__':
    Impresa(1,17,10,2012)
