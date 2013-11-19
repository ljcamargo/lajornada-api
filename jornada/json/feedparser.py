# -*- coding: utf-8 -*-
'''
Created on 13/05/2012

@author: lcammx
'''


import sys, os

path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))

import logging
from collections import defaultdict
from xml.dom import minidom
from parsing import parsing
import json
import httplib
import constants as const
from linguistics.gramatics.heuristics import Heuristics
from datetime import timedelta, datetime




class FeedParser(parsing):
    
    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)
        pass

       
    
    def getHttpResourceString(self, res):
        a = ""; s = ""
        date = self.year + "/" + self.month + "/" + self.day + "/"
        
        if res == "dir":
            s = 'www.jornada.unam.mx'
            a =  '/' + date + 'dir.xml'
            
        if res == "portada":
            s = 'movil.jornada.com.mx'
            a =  '/impresa/' + date + 'portada.xml'
            
        if res == "contra":
            s = 'movil.jornada.com.mx'
            a = '/impresa/' + date + 'contra.xml'
            
        if res == "udir":
            s = 'movil.jornada.com.mx'
            a =  '/ultimas/dir.xml'    
            
        if res == "uportada":
            s = 'movil.jornada.com.mx'
            a =  '/ultimas/portada.xml'
            
        if res == "newultimas":
            s = 'www.jornada.com.mx'
            a =  '/ultimas/newsml-g2.xml'   
            
        if res == "cartones":
            s = 'www.jornada.unam.mx'
            a =  '/' + date + 'cartones.xml'
            
        if res == "audion":
            s = 'movil.jornada.com.mx'
            a = '/podcast/principales/'
            
        conn = httplib.HTTPConnection(s, timeout=240)
        txheaders = {   
            'Accept':'text/html,application/xhtml+xml,application/xml',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':s,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'
        }
        logging.info( s+a )
        conn.request("GET", a, headers=txheaders)
        r1 = conn.getresponse()
        logging.info(r1.status)
        logging.info(r1.reason)
        r = r1.read()
        return r

    def getHttpNoteResourceString(self, res, id):
        a = ""; s = ""
        date = self.year + "/" + self.month + "/" + self.day + "/"
            
        if res == "articulo":
            s = 'www.jornada.unam.mx'
            a = '/' + date + id + '.xml'
            
        if res == "uarticulo":
            s = 'movil.jornada.com.mx'
            a = '/ultimas/'+ id + '.xml'
            
        if res == "u2articulo":
            s = 'www.jornada.com.mx'
            a = id.replace('http://www2.jornada.com.mx','')
            
        conn = httplib.HTTPConnection(s, timeout=240)
        txheaders = {   
            'Accept':'text/html,application/xhtml+xml,application/xml',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':s,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'
        }
        logging.info( s+a )
        conn.request("GET", a, headers=txheaders)
        r1 = conn.getresponse()
        logging.info(r1.status)
        logging.info(r1.reason)
        r = r1.read()
        return r
            
    def dumpJsonItems(self, jItems):
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json'
        f = open(filename, 'w')
        logging.info( 'Writting file: %s' % filename )
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
    
    def getNoteUrl(self, noteid):
        if self.server == "unam":
            r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/" + noteid + ".xml"
        if self.server == "movil":
            r = "http://movil.jornada.com.mx/ultimas/"+ noteid + ".xml"
        return r
    
    def getImgUrl(self, imgid):
        if self.server == "unam":
            r = "http://movil.jornada.com.mx/impresa/fotos/"+self.year+"/"+self.month+"/"+self.day+"/" + self.imgSize + "/" + imgid
        if self.server == "movil":
            r = "http://movil.jornada.com.mx/ultimas/fotos/"+self.imgSize + "/" + imgid
        return r
    
    def getSnapUrl(self, imgid):
        if self.server == "unam":
            r = "http://movil.jornada.com.mx/impresa/fotos/"+self.year+"/"+self.month+"/"+self.day+"/" + self.snapSize + "/" + imgid
        if self.server == "movil":
            r = "http://movil.jornada.com.mx/ultimas/fotos/"+self.snapSize + "/" + imgid
        return r
    
    def getImgOriginalUrl(self, imgid):
        r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/"  + imgid
        return r
    
    def getNavUrl(self, id):
        section = ""
        if len(id)<1 : id = ""
        if "pol" in id:
            section = "politica"
        if "eco" in id:
            section = "economia"
        if "est" in id:
            section = "estados"  
        if "mun" in id:
            section = "mundo"
        if "cap" in id:
            section = "capital"
        if "soc" in id:
            section = "sociedad"
        if "cul" in id:
            section = "cultura"
        if "cie" in id:
            section = "ciencias"
        if "esp" in id:
            section = "espectaculos"   
        if "dep" in id:
            section = "deportes"                                                                                                             
        r = "http://www.jornada.unam.mx/"+section+"/"+self.year+"/"+self.month+"/"+self.day+"/"  + id
        return r
    
    def getUNavUrl(self, id):
        r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/"  + id
        return r
    
    def getU2NavUrl(self, id):
        r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/"  + id
        return r
    
    def getCorrectedType(self, mtype):
        if mtype == "Analysis":
            return "columna"
        if mtype == "Actuality":
            return "noticia"
        if mtype == "Opinion":
            return "columna"
        if mtype == "portada":
            return "noticia"
        if mtype == "contra":
            return "noticia"
        return mtype
    
    def getHtmlPriority(self, mtype):
        if mtype == "h1":
            return 5
        if mtype == "h2":
            return 4
        if mtype == "h3":
            return 3
        if mtype == "h4":
            return 2
        if mtype == "h5":
            return 1
        return mtype
    
    def getImagesObject(self, medialst):
        imgs = []
        url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
        ikind="content"
        for mediaitem in medialst:
            if mediaitem.getAttribute('media-type') == 'image':
                for innermediaitem in mediaitem.childNodes:
                    if innermediaitem.nodeName == 'media-reference':
                        iid = innermediaitem.getAttribute('id')
                        alt = innermediaitem.getAttribute('alternate-text') 
                    if innermediaitem.nodeName == 'media-caption':
                        caption = self.getText(innermediaitem.childNodes)
                    if innermediaitem.nodeName == 'media-producer':
                        author = self.getText(innermediaitem.childNodes)
            url = self.getImgUrl(iid)
            snap = self.getSnapUrl(iid)
            img = {
                   "id":iid,
                   "url":url,
                   "snap":snap,
                   "alt":alt,
                   "caption":caption,
                   "header":header,
                   "author":author,
                   "kind":ikind,
                   }
            imgs.append(img)
        return imgs
           
    def getNewImagesObject(self, medialst):
        imgs = []
        url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
        ikind="content"
        for mediaitem in medialst:
            for innermediaitem in mediaitem.childNodes:
                if innermediaitem.nodeName == 'media-reference':
                    iid = innermediaitem.getAttribute('source')
                    alt = innermediaitem.getAttribute('alternate-text') 
                if innermediaitem.nodeName == 'media-caption':
                    caption = self.getText(innermediaitem.childNodes)
                if innermediaitem.nodeName == 'media-producer':
                    author = self.getText(innermediaitem.childNodes)
            url = iid
            snap = iid
            img = {
                   "id":iid,
                   "url":url,
                   "snap":snap,
                   "alt":alt,
                   "caption":caption,
                   "header":header,
                   "author":author,
                   "kind":ikind,
                   }
            imgs.append(img)
        return imgs
    
    def getNoteContent(self, noteid):
        heur = Heuristics('esp')
        jHNoteContent = []
        jHNoteOddness = defaultdict(int)
        jHNoteKeywords = defaultdict(int)
        jHNoteAbstracted = []
        jHNoteFinalKeywords = []
        filestr = self.getHttpNoteResourceString('articulo', noteid)
        xmldoc = minidom.parseString(filestr)
        
        titlelst  = xmldoc.getElementsByTagName('title')[0].childNodes
        title = {
            "html" :  self.getHtmlFromParragraphs(titlelst),
            "plain" : self.getRecursiveText(titlelst),
            "list" : self.getListItems(titlelst)
                 }
        self.appendNodeToHeuristics(heur,titlelst, jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
        
        hedlinelst = xmldoc.getElementsByTagName('hedline')[0].childNodes
        hedline = {
            "html" :  self.getHtmlFromParragraphs(hedlinelst),
            "plain" : self.getRecursiveText(hedlinelst),
            "list" : self.getListItems(hedlinelst)         
                }
        self.appendNodeToHeuristics(heur,hedlinelst, jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)        
        
        byline = self.getRecursiveText(xmldoc.getElementsByTagName('byline')[0].childNodes[0])
        
        abstractlst = xmldoc.getElementsByTagName('abstract')[0].childNodes
        abstract = {
            "html" :  self.getHtmlFromParragraphs(abstractlst),
            "plain" : self.getRecursiveText(abstractlst),
            "list" : self.getListItems(abstractlst)
            }
        self.appendNodeToHeuristics(heur,abstractlst, jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
        
        bodycontent = xmldoc.getElementsByTagName('body.content')[0].childNodes
        text = {
            "html" :  self.getHtmlFromParragraphs(bodycontent),
            "plain" : self.getRecursiveText(bodycontent),
            "list" : self.getListItems(bodycontent)       
            }
        self.appendNodeToHeuristics(heur,bodycontent, jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
            
        medialst = xmldoc.getElementsByTagName('media')
        imgs = self.getImagesObject(medialst)
        
        for img in imgs:     
            if not img['alt'] is None: self.appendNodeToHeuristics(heur,img['alt'], jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
            if not img['header'] is None: self.appendNodeToHeuristics(heur,img['header'], jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
            if not img['caption'] is None: self.appendNodeToHeuristics(heur,img['caption'], jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
            if not img['author'] is None: self.appendNodeToHeuristics(heur,img['author'], jHNoteContent, jHNoteOddness, jHNoteKeywords, jHNoteAbstracted)
        
            
        jHAbstractedString = ''.join(jHNoteAbstracted)
        heur._matchDictToList(jHNoteKeywords, jHNoteFinalKeywords)
        heur._matchDictToList(jHNoteOddness, jHNoteFinalKeywords)
        jHNote = { noteid : { "words" : jHNoteContent, "incidence" : jHNoteKeywords, "oddity": jHNoteOddness, "abstracted": jHAbstractedString, "keywords": jHNoteFinalKeywords } }
        self.jMaster = heur.appendToMaster(4,self.jMaster, jHNoteKeywords)
        self.jMaster = heur.appendToMaster(4,self.jMaster, jHNoteOddness)
        self.jHeuristics.append(jHNote)
        self.jAbstracted += "|" + jHAbstractedString

            
        Note = {
                 "id": noteid,
                 "title": title,
                 "hedline": hedline,
                 "byline": byline,
                 "abstract": abstract,
                 "text": text,
                 "images": imgs,
                 "keywords": jHNoteFinalKeywords
        } 
        
        

        return Note
    
