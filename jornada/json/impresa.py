'''
Created on 13/05/2012

@author: lcammx
'''
import sys
sys.path.append('/home/lsjcp/www/modules')

from collections import defaultdict
from xml.dom import minidom
from parsing import parsing
import json
import httplib
import operator
import constants as const
from collections import OrderedDict
from operator import itemgetter
from linguistics.gramatics.esp import ESP
from linguistics.gramatics.heuristics import Heuristics
from datetime import timedelta, datetime

class Impresa(parsing):
    
    def __init__(self, minus=0, day=0, month=0, year=0):
        now = datetime.now()
        if (day!=0 or month!=0 or year!=0):
            now = datetime.now()
        elif minus!=0:
            now = datetime.now()-timedelta(days=minus)        
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
        
        jItems = []
        self.jAnalytics = []
        self.jHeuristics = []
        self.jMaster = defaultdict(int)
        try:
            jItems = self.getNoteItemsFromDir(jItems)
            jItems = self.getNoteItemsFromPortada(jItems)
            jItems = self.getNoteItemsFromContra(jItems)
            jItems = self.getNoteItemsFromCartones(jItems)
            jItems = self.getNoteItemsFromAudioN(jItems)
        except Exception as e:
            status="error"
            jItems = []
            self.dumpErrorLog(e)
        else:    
            date = "" + str(self.year) + "/" + str(self.month) + "/" + str(self.year)
            #orderedItems = OrderedDict(sorted(jItems,  key=lambda k: k.iteritems()))
            jOmNews = { 
               "title": const.DELIVERY_DESCRIPTION,
               "publication": const.PUB_NAME,
               "isbn": const.PUB_ISBN,
               "periodicity": const.PUB_PERIODICITY,
               "gentime": const.PUB_GENTIME,
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
               "alias": const.DELIVERY_ALIAS, 
               "contentKind": const.DELIVERY_KIND,
               "status" : status,   
               "content": jItems,
               }
            self.dumpJsonItems([jOmNews])
            try:
                '''Experimental'''
                #heur = Heuristics('esp')
                #heur.findProbableAdjacent(self.jMaster,4,2,self.jHeuristics)
                ''''''
                mtitle = { "title": date }
                environ = { "environment" : self.jHeuristics}
                masterw = { "general" : self.jMaster }
                self.jAnalytics.append(mtitle)
                self.jAnalytics.append(masterw)
                self.jAnalytics.append(environ)
                self.dumpJsonHeuristics(self.jAnalytics)
            except Exception as error2:
                self.dumpErrorLog(error2)
    
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
        print s+a
        conn.request("GET", a, headers=txheaders)
        r1 = conn.getresponse()
        print r1.status, r1.reason
        r = r1.read()
        #print r
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
            
        conn = httplib.HTTPConnection(s, timeout=240)
        txheaders = {   
            'Accept':'text/html,application/xhtml+xml,application/xml',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':s,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'
        }
        print s+a
        conn.request("GET", a, headers=txheaders)
        r1 = conn.getresponse()
        print r1.status, r1.reason
        r = r1.read()
        print r
        return r
            
    def dumpJsonItems(self, jItems):
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=True)
        filename = const.SAVING_ROUTE + const.SAVING_NAME + self.year + '_' + self.month + '_' + self.day + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def dumpJsonHeuristics(self, jItems):
        j =  json.dumps(jItems, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + const.SAVING_HEURISTICS_NAME + self.year + '_' + self.month + '_' + self.day + '.json'
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
        filename = const.SAVING_ROUTE + const.SAVING_ERROR_NAME + self.year + '_' + self.month + '_' + self.day + '_' + now.strftime("%H_%M_%S") + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
    
    def getNoteUrl(self, noteid):
        if self.server == "unam":
            r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/" + noteid + ".xml"
        return r
    
    def getImgUrl(self, imgid):
        if self.server == "unam":
            r = "http://movil.jornada.com.mx/impresa/fotos/"+self.year+"/"+self.month+"/"+self.day+"/" + self.imgSize + "/" + imgid
        return r
    
    def getSnapUrl(self, imgid):
        if self.server == "unam":
            r = "http://movil.jornada.com.mx/impresa/fotos/"+self.year+"/"+self.month+"/"+self.day+"/" + self.snapSize + "/" + imgid
        return r
    
    def getImgOriginalUrl(self, imgid):
        r = "http://www.jornada.unam.mx/"+self.year+"/"+self.month+"/"+self.day+"/"  + imgid
        return r
    
    def getCorrectedType(self, mtype):
        if mtype == "Analysis":
            return "columna"
        if mtype == "Actuality":
            return "noticia"
        if mtype == "Opinion":
            return "columna"
        return mtype
        
    def getNoteItemsFromDir(self, jItems):
        family = "dir"
        #filen = self.getResourceRoute('dir')
        filestr = self.getHttpResourceString('dir')
        #xmldoc = minidom.parse(filen)
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            titlelst = node.getElementsByTagName('title')
            title = ""
            for titles in titlelst:
                title = self.getText(titles.childNodes)
            print 'noteid '   + nodeid 
            
            print "title: "  + title   
            
            firstplst = node.getElementsByTagName('firstp')
            summary = self.getArray(firstplst)
            
            serieslst = node.getElementsByTagName('series')
            series = ""
            for  seriesitem in serieslst:
                series += self.getText(seriesitem.childNodes)
            
            authorlst = node.getElementsByTagName('author')
            author = ""
            for authoritem in authorlst:
                author = self.getText(authoritem.childNodes)
            
            datelst = node.getElementsByTagName('date')
            date = ""
            for dateitem in datelst:
                date = self.getText(dateitem.childNodes)
            
            medialst = node.getElementsByTagName('media')
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
                
            abstractlst = node.getElementsByTagName('abstract')
            abstract = self.getArray(abstractlst)
            #for abstractitem in abstractlst:
                #abstract += self.getText(abstractitem.childNodes) 
                
            #EACH NOTE PARSING
            notecontent = self.getNoteContent(nodeid)
            
            jItem = {
                     "id": nodeid,
                     "order":x,
                     "family": family,
                     "section": section,
                     "type": type,
                     "noteXmlUrl": noteXmlUrl,
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
                     "content": notecontent
            }    
            jItems.append(jItem)
    
        #RAYUELA
        rayuela = xmldoc.getElementsByTagName('Rayuela')[0]
        nodeid = ""
        noteXmlUrl =  ""
        section = "rayuela"
        stype = "bullet"
        title = self.getRecursiveText(rayuela)
        summary = []
        series = "rayuela"
        author = ""
        date = ""
        imgs = []
        abstract = ""    
        new = {
             "id": nodeid,
             "order": 0,
             "family": family,
             "section": section,
             "type": stype,
             "noteXmlUrl": noteXmlUrl,
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
        jItems.append(new)
        
        jItems= sorted(jItems,  key=lambda k: k['order'])   
        return jItems
    
    
        
    def getNoteItemsFromPortada(self, jItems):
        family = "portada"
        #filen = self.getResourceRoute('portada')
        #filestr = self.getHttpResourceString('portada')
        #xmldoc = minidom.parse(filen)
        filestr = self.getHttpResourceString('portada')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            nodeid = node.getAttribute('id')
            noteXmlUrl =  self.getNoteUrl(nodeid)
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            titlelst = node.getElementsByTagName('title')
            title = ""
            for titles in titlelst:
                title = self.getText(titles.childNodes)
            print 'noteid '   + nodeid    
            
            summary = []
            firstplst = node.getElementsByTagName('firstp')
            summary = self.getArray(firstplst)
            #for firstp in firstplst:
                #for innerfirsts in firstp.childNodes:
                    #summary.append(self.getText(innerfirsts.childNodes))

            serieslst = node.getElementsByTagName('series')
            series = ""
            for  seriesitem in serieslst:
                series += self.getText(seriesitem.childNodes)
            
            authorlst = node.getElementsByTagName('author')
            author = ""
            for authoritem in authorlst:
                author = self.getText(authoritem.childNodes)
            
            datelst = node.getElementsByTagName('date')
            date = ""
            for dateitem in datelst:
                date = self.getText(dateitem.childNodes)
            
            medialst = node.getElementsByTagName('media')
            imgs = []
            url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
            ikind = "main"
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
                       "kind":ikind
                       }
                imgs.append(img)
                
            abstractlst = node.getElementsByTagName('abstract')
            abstract = self.getArray(abstractlst)
            #for abstractitem in abstractlst:
                #abstract += self.getText(abstractitem.childNodes)
                
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
                         "order": x,
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
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
                         "content": jItems[i].get('content')
                    }
                    jItems[i] = new
                    x += 1

        orphanpics = xmldoc.getElementsByTagName('foto')
        y = 0
        for node in orphanpics:
            nodeid = ""
            noteXmlUrl =  ""
            section = ""
            stype = "orphan_photo"
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
                 "order": y,
                 "family": family,
                 "section": section,
                 "type": stype,
                 "noteXmlUrl": noteXmlUrl,
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
            section = node.getAttribute('section')
            type = node.getAttribute('type')
            type = self.getCorrectedType(type)
            
            titlelst = node.getElementsByTagName('title')
            title = ""
            for titles in titlelst:
                title = self.getText(titles.childNodes)
            print 'noteid '   + nodeid    
            
            summary = []
            firstplst = node.getElementsByTagName('firstp')
            summary = self.getArray(firstplst)

            serieslst = node.getElementsByTagName('series')
            series = ""
            for  seriesitem in serieslst:
                series += self.getText(seriesitem.childNodes)
            
            authorlst = node.getElementsByTagName('author')
            author = ""
            for authoritem in authorlst:
                author = self.getText(authoritem.childNodes)
            
            datelst = node.getElementsByTagName('date')
            date = ""
            for dateitem in datelst:
                date = self.getText(dateitem.childNodes)
            
            medialst = node.getElementsByTagName('media')
            imgs = []
            url = ""; snap=""; alt = ""; caption = ""; header =""; author = ""; ikind=""; iid =""
            ikind = "main"
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
                       "kind":ikind
                       }
                imgs.append(img)
                
            abstractlst = node.getElementsByTagName('abstract')
            abstract = self.getArray(abstractlst)
            #for abstractitem in abstractlst:
                #abstract += self.getText(abstractitem.childNodes) + '\n'
                
            for i in xrange(len(jItems)-1,-1,-1):
                if jItems[i].get('id') == nodeid:
                    preimgs = jItems[i].get('images')
                    if len(preimgs)>0:
                        for ii in xrange(len(preimgs)-1,-1,-1):
                            for iii in xrange(len(imgs)-1,-1,-1):
                                if preimgs[ii].get('id') == imgs[iii].get('id'):
                                    preimgs[ii] = imgs[iii]
                                    #print "-------------------merged images " + imgs[iii].get('id')      
                                else:
                                    preimgs.append(imgs[iii])
                                    #print "-------------------not merged " + imgs[iii].get('id')
                    else:
                        preimgs = imgs
                    new = {
                         "id": nodeid,
                         "order": x,
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
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
                         "content": jItems[i].get('content')
                    }
                    jItems[i] = new
                    x += 1 

        orphanpics = xmldoc.getElementsByTagName('foto')
        
        y = 0
        for node in orphanpics:
            nodeid = ""
            noteXmlUrl =  ""
            section = ""
            stype = "orphan_photo"
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
                 "order": y,
                 "family": family,
                 "section": section,
                 "type": stype,
                 "noteXmlUrl": noteXmlUrl,
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
            type = node.getAttribute('cartones')

            curl=""
            urllst = node.getElementsByTagName('url')[0].childNodes[0]
            curl = urllst.nodeValue
            print 'url '   + curl    
            
            cthumb=""
            thumblst = node.getElementsByTagName('thumbnail')[0].childNodes[0]   
            cthumb = thumblst.nodeValue
            print 'thumb '   + cthumb    
            
            cauthor=""
            authorlst = node.getElementsByTagName('author')[0].childNodes[0]   
            cauthor = authorlst.nodeValue
            print 'author '   + cauthor    
            
            ccaption=""
            captionlst = node.getElementsByTagName('caption')[0].childNodes[0]   
            ccaption = captionlst.nodeValue
            print 'caption '   + ccaption    

            curl = self.getImgOriginalUrl(curl)
            cthumb = self.getImgOriginalUrl(cthumb)
            
            imgs = []
            ikind = "main"
            
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
                         "order": x,
                         "family": family,
                         "section": section,
                         "type": type,
                         "noteXmlUrl": noteXmlUrl,
                         "title": ccaption,
                         "edTitle": ccaption,
                         "summary": cauthor,
                         "edSummary": cauthor,
                         "abstract": "",
                         "series": "",
                         "author": cauthor,
                         "date": "",
                         "audio":"",
                         "images": img
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
            print 'guid '   + guid    
            
            audio=""
            enclosure = node.getElementsByTagName('enclosure')[0]
            audio = enclosure.getAttribute('url')
            print 'audio '   + audio    
                          
            for i in xrange(len(jItems)-1,-1,-1):
                if jItems[i].get('id') == guid:
                    new = {
                         "id": jItems[i].get('id'),
                         "order": jItems[i].get('order'),
                         "family": jItems[i].get('family'),
                         "section": jItems[i].get('section'),
                         "type": jItems[i].get('type'),
                         "noteXmlUrl": jItems[i].get('noteXmlUrl'),
                         "title": jItems[i].get('title'),
                         "edTitle": jItems[i].get('edTitle'),
                         "summary": jItems[i].get('summary'),
                         "edSummary": jItems[i].get('edSummary'),
                         "abstract": jItems[i].get('abstract'),
                         "series": jItems[i].get('series'),
                         "author": jItems[i].get('author'),
                         "date": jItems[i].get('date'),
                         "audio":audio,
                         "images": jItems[i].get('images'),
                         "content": jItems[i].get('content'),
                         
                    }
                    jItems[i] = new
              
        return jItems
    
    def getNoteContent(self, noteid):
        heur = Heuristics('esp')
        jHNoteContent = []
        jHNoteKeywords = defaultdict(int)
        filestr = self.getHttpNoteResourceString('articulo', noteid)
        xmldoc = minidom.parseString(filestr)
        print "noteid::::"+noteid
        #title = ""
        title = self.getRecursiveText(xmldoc.getElementsByTagName('title')[0].childNodes[0])
        print 'head ' + title
        
        hedline = []
        hedlinelst = xmldoc.getElementsByTagName('hedline')[0].childNodes
        for hedlineitem in hedlinelst:
            hedlineitxt = ""
            if hedlineitem.nodeName == 'hl1':
                hedlineitxt = self.getRecursiveText(hedlineitem)
            if hedlineitem.nodeName == 'hl2':
                hedlineitxt = self.getRecursiveText(hedlineitem)
            if hedlineitxt != '':
                if hedlineitxt != None:
                    hedline.append(hedlineitxt)
                    print "hedline " + hedlineitxt
        
        
        byline = self.getRecursiveText(xmldoc.getElementsByTagName('byline')[0].childNodes[0])
        #byline = xmldoc.getElementsByTagName('byline')[0].childNodes[0].nodeValue
        
        abstract = self.getArray(xmldoc.getElementsByTagName('abstract')[0].childNodes)
        #abslst = xmldoc.getElementsByTagName('abstract')[0].childNodes
        #for absitem in abslst:
            #absitxt = ""
            #absitxt = self.getText(absitem)
            #if absitxt != None:
                #abstract.append(absitxt)
                #print 'abstract ' + absitxt
        
        parragraphs = []
        bodycontent = xmldoc.getElementsByTagName('body.content')[0].childNodes
        #body = xmldoc.getElementsByTagName('body.content')[0]
        #text = bodycontent.toxml()
        text = ""
        for bodycitem in bodycontent:
            if bodycitem.nodeName=='p':
                text += bodycitem.toxml()
                inp = ""
                inp = self.getRecursiveText(bodycitem)
                if inp != None:
                    if inp != '':
                        jHNoteContent = heur.matchTextToList(inp, jHNoteContent)
                        jHNoteKeywords = heur.matchTextToDict(inp, jHNoteKeywords)
                        parragraphs.append(inp)      
                    
        imgs = []
        medialst = xmldoc.getElementsByTagName('media')
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
            
        jHNoteKeywords = heur.matchTextToDict(title, jHNoteKeywords)
        jHNoteKeywords = heur.matchArrayToDict(hedline, jHNoteKeywords) 
        jHNoteKeywords = heur.matchTextToDict(byline, jHNoteKeywords)
        jHNoteKeywords = heur.matchArrayToDict(abstract, jHNoteKeywords)
        
        jHNoteContent = heur.matchTextToList(title, jHNoteContent)                         
        jHNoteContent = heur.matchArrayToList(hedline, jHNoteContent)
        jHNoteContent = heur.matchTextToList(byline, jHNoteContent)
        jHNoteContent = heur.matchArrayToList(abstract, jHNoteContent)
        jHNote = { noteid : { "words" : jHNoteContent, "freqs" : jHNoteKeywords } }
        self.jMaster = heur.appendToMaster(4,self.jMaster,jHNoteKeywords)
        self.jHeuristics.append(jHNote)

            
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
    Impresa()