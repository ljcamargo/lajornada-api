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

class UltimasXmlW8(FeedParser):
    
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
        self.xmlcontent = "";
        self.xmlItems = "";
        
        jItems = self.getNoteItemsFromUPortada(jItems)
   

        self.dumpW8XmlItems()
        
                
    def dumpW8XmlItems(self):
        self.setHistoricFile()
        self.xmlcontent = "<?xml version='1.0' encoding='utf-8' ?><tile><visual>"
        self.xmlcontent += self.xmlItems
        self.xmlcontent += "</visual></tile>"
        filename = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'last_w8.xml'
        f = open(filename, 'w')
        print 'writting: %s' % filename
        f.write(self.xmlcontent.encode('utf-8'))
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
        current = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'last_w8.xml'
        historic = const.SAVING_ROUTE + '/' +  const.SAVING_NAME_CURRENT + 'prev_w8.xml'
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
    
        
    def getNoteItemsFromUPortada(self, jItems):
        filestr = self.getHttpResourceString('uportada')
        xmldoc = minidom.parseString(filestr)
        directory = xmldoc.getElementsByTagName('Item')
        x = 0
        for node in directory:
            x += 1
            xmlitem = ""
            title = self.getRecursiveText(node.getElementsByTagName('title'))
            
            medialst = node.getElementsByTagName('media')
            fi = ""
            for mediaitem in medialst:
                if mediaitem.getAttribute('media-type') == 'image':
                    for innermediaitem in mediaitem.childNodes:
                        if innermediaitem.nodeName == 'media-reference':
                            iid = innermediaitem.getAttribute('id')
                fi = self.getSnapUrl(iid)
            
            
            xmltxt = "<text id='" + str(x) + "'>" + title +"</text>"
            xmlimg = "<image id='" + str(x) + "' src='" + fi +"' />"
            if fi != "":
                xmlitem = "<binding template='TileWideImageAndText01'>"
                xmlitem += xmltxt + xmlimg
                xmlitem += "</binding>"
            else:
                xmlitem = "<binding template='TileWideText01'>"
                xmlitem += xmltxt
                xmlitem += "</binding>"
            self.xmlItems += xmlitem
                

        orphanpics = xmldoc.getElementsByTagName('foto')
        y = 0
        for node in orphanpics:
            y += 1
            xmlitem = ""
            title = node.getAttribute('cabeza')
            snap = self.getSnapUrl(node.getAttribute('src'))
            if snap.count("http")>1 : snap = ""
            xmltxt = "<text id='" + str(x) + "'>" + title +"</text>"
            xmlimg = "<image id='" + str(x) + "' src='" + fi +"' />"
            if snap != "":
                xmlitem = "<binding template='TileWideImage01'>"
                xmlitem += xmlimg
                xmlitem += "</binding>"
            self.xmlItems += xmlitem
            
                                                    
               
if __name__ == '__main__':
    UltimasXmlW8()
