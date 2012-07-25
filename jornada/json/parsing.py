# -*- coding: utf-8 -*-
'''
Created on 13/05/2012

@author: lcammx
'''


import re
from lxml.html.clean import clean_html

class parsing(object):
    
    def __init__(self):
        '''constructor'''
            
    def dumpJsonItems(self, jItems):
        '''method'''
        
    def dumpErrorLog(self, error):
        '''method'''
    
    def getText(self, nodelist):
            rc = []
            try:
                mem = ""
                for node in nodelist: 
                    if node.nodeType == node.TEXT_NODE:
                        val = node.nodeValue
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace(): 
                                if len(val)<2: 
                                    mem = val
                                else:                                
                                    rc.append(mem+val)
                                    mem = ""
            except:
                rci = nodelist.nodeValue
                return rci
            str = ''.join(rc)
            return str.strip() 
        
    def getRecursiveText(self, nodelist):
            rc = []
            if hasattr(nodelist, 'hasChildNodes'):
                if nodelist.hasChildNodes():
                    for node in nodelist.childNodes: 
                        val = self.getRecursiveText(node)
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace():                              
                                rc.append(val+ "  ")
                else:
                    if nodelist.nodeType == nodelist.TEXT_NODE:
                        val = self.getLastText(nodelist)                   
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace():                              
                                rc.append(val+ "  ")            
            else:
                for nodeitem in nodelist:
                    val = self.getRecursiveText(nodeitem)
                    if val != None:
                        val = val.strip()
                        if val != "" and not val.isspace():                              
                            rc.append(val+ "  ")
            return self.joinLines(rc, "\r \r", 1)
    
    def getIntFromText(self, text):
        text = text.strip()
        text = re.sub("[^0-9]", "", text)
        return int(text)
        
    def getLastText(self, node):
            rc = ""
            try:
                val = node.nodeValue
                if val != None:
                    val = val.strip()
                    if val != "" and not val.isspace(): 
                        rc+=val                    
            except Exception as e:
                rci = e.__str__()
                return rci
            return rc
    
    def getArray(self, nodelist):
            rc = []
            try:
                mem = ""
                for node in nodelist: 
                    if node.hasChildNodes():
                        for nnode in node.childNodes:
                            val = self.getRecursiveText(nnode)
                            if val != None:
                                val = val.strip()
                                if val != "" and not val.isspace(): 
                                    if len(val)<2: 
                                        mem = val
                                    else:                                
                                        rc.append(mem+val)
                                        mem = ""
                    else:
                        val = node.nodeValue
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace(): 
                                if len(val)<2: 
                                    mem = val
                                else:                                
                                    rc.append(mem+val)
                                    mem = ""                   
            except Exception as e:
                rci = e.__str__()
                return [rci]
            return rc

    def getHtmlFromParragraphs(self, content):
        text = ""
        if isinstance(content, list):
            for item in content:
                if hasattr(item, 'nodeName'):
                    val =  item.toxml()
                    if val != None:
                        val = val.strip()
                        if val != "" and not val.isspace():   
                            text += val
        else:
            if hasattr(content, 'hasChildNodes'):
                if content.hasChildNodes():
                    for child in content.childNodes:
                        val =  item.toxml()
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace():   
                                text += val
            else:
                val =  item.toxml()
                if val != None:
                    val = val.strip()
                    if val != "" and not val.isspace():   
                        text += val
        text = clean_html(text)
        return text
            
    def joinLines(self, lst, breaker, minimus):
        txt = ""
        for i in range(len(lst)):
            txt += lst[i]
            if i<(len(lst)-1):
                if len(lst[i])>1:
                    txt+= breaker
        return txt
    
    def getListItems(self, content):
        rlist = []
        
        if isinstance(content, list):
            mem = ""
            for item in content:
                itxt = ""
                itxt = self.getRecursiveText(item)
                if itxt != None:
                    itxt = itxt.strip()
                    if itxt != "" and not itxt.isspace():
                        if len(itxt)>2:
                            rlist.append(mem+itxt)
                            mem = ""
                        else:
                            mem = itxt
            if len(mem)>0: rlist.append(mem)
        else :
            rlist.append(self.getRecursiveText(content))
        return rlist
    
    
    def appendNodeToHeuristics(self, heuristics, node, words, oddness,keywords):
        for item in node:
            if item.nodeName=='p':
                inp = self.getRecursiveText(item)
                if inp != None:
                    if inp != '':
                        heuristics._matchTextToList(inp, words)
                        heuristics._proccessOddness(inp, oddness)
                        heuristics._matchTextToDict(inp, keywords)     