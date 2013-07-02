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
from linguistics.gramatics.heuristics import Heuristics
from datetime import timedelta, datetime
from feedparser import FeedParser
class Ultimas(FeedParser):
    
    def __init__(self, minus=0, day=0, month=0, year=0):
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
        
        jItems = []
        
        jItems = self.getNoteItemsFromUPortada(jItems)
        jItems = self.getNoteItemsFromUDir(jItems)
        
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
        print 'writting: %s' % filename
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
    
        
        
    def getNoteItemsFromUDir(self, jItems):
        family = "udir"
        filestr = self.getHttpResourceString('udir')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 100
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            navUrl = self.getUNavUrl(nodeid)
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
            
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('date'))           
            
            medialst = node.getElementsByTagName('media')
            imgs = self.getImagesObject(medialst)
                
            #EACH NOTE PARSING
            notecontent = self.getUNoteContent(nodeid)
            
            jItem = {
                     "id": nodeid,
                     "index":x,
                     "page":1,
                     "order":x,
                     "priority": 6,
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
    
    
        
    def getNoteItemsFromUPortada(self, jItems):
        family = "uportada"
        filestr = self.getHttpResourceString('uportada')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            navUrl = self.getUNavUrl(nodeid)
            section = node.getAttribute('section')
            type="noticia"
            priority = node.getAttribute('type')
            priority = self.getHtmlPriority(type)
            
            title = self.getRecursiveText(node.getElementsByTagName('title'))
            firstplst = node.getElementsByTagName('firstp')
            summary = {
                "html" :  self.getHtmlFromParragraphs(firstplst),
                "plain" : self.getRecursiveText(firstplst),
                "list" : self.getListItems(firstplst)
            }      
            
            author = self.getRecursiveText(node.getElementsByTagName('author'))        
            date = self.getRecursiveText(node.getElementsByTagName('date'))
            
            medialst = node.getElementsByTagName('media')
            imgs = self.getImagesObject(medialst)
                      
            added = False
            for i in xrange(len(jItems)-1,-1,-1):
                #LOOP ALL ITEMS
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
                         "page": 0,
                         "order": x,
                         "priority": priority,
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
                         "navUrl": navUrl,
                         "title": jItems[i].get('title'),
                         "edTitle": title,
                         "summary": jItems[i].get('summary'),
                         "edSummary": summary,
                         "abstract": "",
                         "series": "",
                         "author": author,
                         "date": date,
                         "audio":"",
                         "images": preimgs,
                         "content": jItems[i].get('content')
                    }
                    jItems[i] = new
                    added = True
                else:
                    pass
                
            if (added == False):               
                #NOT ADDED, APPEND AS NEW     
                notecontent = self.getUNoteContent(nodeid)
                jItem = {
                         "id": nodeid,
                         "index":x,
                         "page":0,
                         "order":x,
                         "priority": priority,
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
                         "series": "",
                         "author": author,
                         "date": date,
                         "audio":"",
                         "images": imgs,
                         "content": notecontent
                }    
                jItems.append(jItem)
            x += 1   

        orphanpics = xmldoc.getElementsByTagName('foto')
        y = 0
        for node in orphanpics:
            nodeid = ""
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
                 "priority": "",
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
                 "content": []
            }
            
            #HARDCODE VETOED ELEMENT: EL DIA EN IMAGENES
            if (title!=u"El día en imágenes"):
                jItems.append(new)
            y += 1
                                              
        jItems= sorted(jItems,  key=lambda k: k['order'])              
        return jItems
    
    
    def getUNoteContent(self, noteid):
        heur = Heuristics('esp')
        jHNoteContent = []
        jHNoteOddness = defaultdict(int)
        jHNoteKeywords = defaultdict(int)
        filestr = self.getHttpNoteResourceString('uarticulo', noteid)
        xmldoc = minidom.parseString(filestr)
        
        titlelst  = xmldoc.getElementsByTagName('title')[0].childNodes
        title = {
            "html" :  self.getHtmlFromParragraphs(titlelst),
            "plain" : self.getRecursiveText(titlelst),
            "list" : self.getListItems(titlelst)
                 }
        #self.appendNodeToHeuristics(heur,titlelst, jHNoteContent, jHNoteOddness, jHNoteKeywords)
        
        hedlinelst = xmldoc.getElementsByTagName('hedline')[0].childNodes
        hedline = {
            "html" :  self.getHtmlFromParragraphs(hedlinelst),
            "plain" : self.getRecursiveText(hedlinelst),
            "list" : self.getListItems(hedlinelst)         
                }
        
        #self.appendNodeToHeuristics(heur,hedlinelst, jHNoteContent, jHNoteOddness, jHNoteKeywords)        
        
        byline = self.getRecursiveText(xmldoc.getElementsByTagName('byline')[0].childNodes[0])
        
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
        imgs = self.getImagesObject(medialst)

            
        Note = {
                 "id": noteid,
                 "title": title,
                 "hedline": hedline,
                 "byline": byline,
                 "abstract": abstract,
                 "text": text,
                 "images": imgs
        } 
        
        
        

        return Note
    
    

           
               
if __name__ == '__main__':
    Ultimas()
