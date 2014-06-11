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
import logging
from operator import itemgetter
from linguistics.gramatics.heuristics import Heuristics
from datetime import timedelta, datetime
from feedparser import FeedParser
import httplib
import urllib



class Ultimas(FeedParser):
    
    def __init__(self, minus=0, day=0, month=0, year=0):
        logging.getLogger().setLevel(logging.INFO)
        now = datetime.now()
        if (day!=0 or month!=0 or year!=0):
            now = datetime.now()
        elif minus!=0:
            now = datetime.now()-timedelta(days=minus)        
        status="success"
        self.server = "movil"
        self.year = str(now.year)
        self.month = str(now.month)
        if len(self.month) < 2:
            self.month = "0"+self.month     
        self.day = str(now.day)
        if len(self.day) < 2:
            self.day = "0"+self.day 
        self.imgSize = const.CONFIG_IMGSIZE
        self.snapSize = const.CONFIG_SNAPSIZE
        self.superfamily = "ultimas"
        
        self.carousel = []
        self.cover = []
        self.daily = []
        jItems = []
        
        self.daily = self.getDaily()
        self.carousel = self.getCarousel()
        self.cover = self.getCover()

        jItems = self.getNoteItemsFromUPortada(jItems)
        
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        orderedItems = sorted(jItems, key=itemgetter('index'))
        jOmNews = { 
           "title": const.DELIVERY_DESCRIPTION_CURRENT,
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
           "alias": const.DELIVERY_ALIAS_CURRENT, 
           "contentKind": const.DELIVERY_KIND_CURRENT,
           "status" : status,   
           "content": orderedItems,
           }
        self.dumpJsonItems([jOmNews])
        
            
    def dumpJsonItems(self, jItems):
        self.setHistoricFile()
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'last.json'
        f = open(filename, 'w')
        logging.info('writting: %s' % filename)
        f.write(j)
        f.close()
        
        
    def dumpErrorLog(self, error):
        now = datetime.now()
        jError = [{ 
           "title": const.ERROR_TITLE_CURRENT,
           "publication": const.PUB_NAME,
           "time": now.strftime("%Y-%m-%d %H:%M:%S"),
           "alias": const.ERROR_TITLE_CURRENT,
           "message" : error.__str__()
           }]
        j =  json.dumps(jError, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=True)
        filename = const.SAVING_ROUTE + "/" + const.SAVING_ERROR_NAME_CURRENT + self.year + '_' + self.month + '_' + self.day + '_' + now.strftime("%H_%M_%S") + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def setHistoricFile(self):
        current = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'last.json'
        historic = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'prev.json'
        if os.path.isfile(current):
            to_readfile = open(current, 'r')
            try:
                reading_file = to_readfile.read()
                writefile=open(historic, 'w')
                try:
                    writefile.write(reading_file)
                finally:
                    writefile.close()      
            finally:
                to_readfile.close()
    
    def getCarousel(self):
        logging.info('fetch carousel')
        try:
            filestr = self.getHttpResourceString('carousel')
            logging.info(filestr)
            precarousel = json.loads(filestr)
            return precarousel["carousel"]
        except:
            logging.info('could not fetch carousel')
            return False
        
    def getDaily(self):
        logging.info('fetch daily')
        try:
            filestr = self.getHttpResourceString('daily')
            logging.info(filestr)
            predict = json.loads(filestr)
            return predict["dailynews"]
        except:
            logging.info('could not fetch daily')
            return False
        
    def getCover(self):
        logging.info('fetch cover')
        try:
            filestr = self.getHttpResourceString('cover')
            logging.info(filestr)
            predict = json.loads(filestr)
            return predict["cover"]
        except:
            logging.info('could not fetch cover')
            return False       
        
    def noteIsPortada(self, id):
        logging.info(id)
        for item in self.carousel:
            if (item["url"] == id):
                logging.info("------------->found at carousel")
                return True   
        return False
    
    def noteIsCover(self, id):
        logging.info(id)
        for item in self.cover:
            if (item["url"] == id):
                logging.info("------------->found at cover")
                return True   
        return False 
    
    def noteGetUID(self, id):
        logging.info(id)
        for item in self.daily:
            if (item["url"] == id):
                return item["uid"]   
        return ""   
        
    def getNoteItemsFromUPortada(self, jItems):
        logging.info('downloading uportada')
        filestr = self.getHttpResourceString('newultimas')
        logging.info('did download uportada')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('itemRef')
        logging.info('did parsed uportada')
        x = 0
        for node in directory:
            _type = "noticia"
            noteXmlUrl =  node.getAttribute('href')
            noteNitfUrl = noteXmlUrl.replace('newsml-g2.xml','nitf')
            try:
                notecontent = self.getUNoteContent(noteNitfUrl)
            except:
                logging.info("note download fail! ")
                continue
            navUrl = noteXmlUrl.replace('/newsml-g2.xml','')
            family = "ucover" if (self.noteIsCover(navUrl)) else "udir"
            family = "uportada" if (self.noteIsPortada(navUrl)) else family
            nodeid = self.getMicroID(navUrl)
            uid = self.noteGetUID(navUrl)
            nodeid = uid if (uid!="") else nodeid
            section = notecontent.get("section")
            sectionname = notecontent.get("sectionName")
            priority = notecontent.get("priority")
            title = self.getRecursiveText(node.getElementsByTagName('headline'))
            firstplst = node.getElementsByTagName('description')
            summary = {
                "html" :  self.getHtmlFromParragraphs(firstplst),
                "plain" : self.getRecursiveText(firstplst),
                "list" : self.getListItems(firstplst)
            }      
            summary = notecontent.get('abstract')
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('versionCreated'))
            
            imgs = notecontent.get("images")  
                          
            #NOT ADDED, APPEND AS NEW     
            
            jItem = {
                     "id": nodeid,
                     "uid": uid,
                     "index":x,
                     "page":0,
                     "order":x,
                     "priority": priority,
                     "family": family,
                     "section": section,
                     "sectionName": sectionname,
                     "type": _type,
                     "noteXmlUrl": noteXmlUrl,
                     "navUrl": navUrl,
                     "title": title,
                     "edTitle": title,
                     "summary": summary,
                     "edSummary": summary,
                     "abstract": "",
                     "series": "",
                     "author": author,
                     "date": date,
                     "audio":"",
                     "images": imgs,
                     "content": notecontent
            }    
            jItems.append(jItem)
            x += 1   

                                              
        jItems= sorted(jItems,  key=lambda k: k['order'])              
        return jItems
    
    
    def getUNoteContent(self, noteid):
        filestr = self.getHttpNoteResourceString('u2articulo', noteid)
        xmldoc = minidom.parseString(filestr)
        
        priority = xmldoc.getElementsByTagName('urgency')[0].getAttribute('ed-urg')
        section = xmldoc.getElementsByTagName('pubdata')[0].getAttribute('position.section')
        sectionslug = self.getSectionSlug(section)
        
        titlelst  = xmldoc.getElementsByTagName('title')[0].childNodes
        title = {
            "html" :  self.getHtmlFromParragraphs(titlelst),
            "plain" : self.getRecursiveText(titlelst),
            "list" : self.getListItems(titlelst)
                 }
        
        hedlinelst = xmldoc.getElementsByTagName('hedline')[0].childNodes
        hedline = {
            "html" :  self.getHtmlFromParragraphs(hedlinelst),
            "plain" : self.getRecursiveText(hedlinelst),
            "list" : self.getListItems(hedlinelst)         
                }
        
        try:
            byline = self.getRecursiveText(xmldoc.getElementsByTagName('byline')[0].childNodes[0])
        except:
            byline = u'La Jornada'
            
        abstractlst = xmldoc.getElementsByTagName('abstract')[0].childNodes
        abstract = {
            "html" :  self.getHtmlFromParragraphs(abstractlst),
            "plain" : self.getRecursiveText(abstractlst),
            "list" : self.getListItems(abstractlst)
            }
        
        #self.appendNodeToHeuristics(heur,abstractlst, jHNoteContent, jHNoteOddness, jHNoteKeywords)
        
        bodycontent = xmldoc.getElementsByTagName('body.content')[0].childNodes
        text = {
            "html" :  self.getHtmlFromParragraphs(bodycontent),
            "plain" : self.getRecursiveText(bodycontent),
            "list" : self.getListItems(bodycontent)       
            }
            
        medialst = xmldoc.getElementsByTagName('media')
        imgs = self.getNewImagesObject(medialst)

            
        Note = {
                 "id": noteid,
                 "priority": priority,
                 "sectionName":section,
                 "section": sectionslug,
                 "title": title,
                 "hedline": hedline,
                 "byline": byline,
                 "abstract": abstract,
                 "text": text,
                 "images": imgs
        } 
        
        
        

        return Note
    
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
    
    def getSectionSlug(self, name):
        if (name==u'Política'):
            return 'politica'
        elif (name==u'Economía'):
            return 'economia'
        elif (name==u'Estados'):
            return 'estados'
        elif (name==u'Capital'):
            return 'capital'
        elif (name==u'Mundo'):
            return 'mundo'
        elif (name==u'Sociedad y Justicia'):
            return 'sociedad'
        elif (name==u'Ciencias'):
            return 'ciencias'
        elif (name==u'Cultura'):
            return 'cultura'
        elif (name==u'Espectáculos'):
            return 'espectaculos'
        elif (name==u'Deportes'):
            return 'deportes'
        elif (name==u'Multimedia'):
            return 'multimedia'
        else:
            return name
    

           
               
if __name__ == '__main__':
    Ultimas()
