# -*- coding: utf-8 -*-

import json
import os
from linguistics.gramatics.heuristics import Heuristics
from datetime import datetime as dayt
import constants as const
from collections import defaultdict


class Indexation(object):

    def __init__(self, action="", month="", year=""):
        self.action = action if action != None else ""
        self.month = month if month != None else ""
        self.year = year if year != None else ""
        self.json = "" 
        self.jsonr = ""
        self.result = ""
        self.somethingFound = False
        
        if self.action == "month":
            if self.year == "":
                now = dayt.now()
                self.year = str(now.year)
            if self.month == "":
                now = dayt.now()
                self.month = str(now.month)
            self.indexMonth()
        elif self.action == "year":
            if self.year == "":
                now = dayt.now()
                self.year = str(now.year)
            self.indexYear()
        elif self.action == "global":
            self.globalJsonIndexation()
    
    def validateDate(self):
        if self.year>2000 and self.year < dayt().year:
            if self.month<12 and self.month >0:
                if self.day<31 and self.day >0:
                    return True

    def indexMonth(self):
        self.genEmptyTemplate()
        for x in range (1,32):
            self.json = None
            self.day = str(x)
            if self.getJsonHeuristicDay():
                self.somethingFound = True
                self.runRequest()
        if self.somethingFound:
            self.genMonthlyJSON()
            self.dumpJsonMonthlyHeuristics()
        else:    
            self.nothingfound()
            
    def indexYear(self):
        self.genEmptyTemplate()
        for x in range (1,13):
            self.json = None
            self.month = str(x)
            if self.getJsonHeuristicMonth():
                self.somethingFound = True
                self.runRequest()
        if self.somethingFound:
            self.genYearlyJSON()
            self.dumpJsonYearlyHeuristics()
        else:    
            self.nothingfound()
                           
    def getJsonHeuristicDay(self):
        if len(self.month) < 2:
            self.month = "0"+self.month     
        if len(self.day) < 2:
            self.day = "0"+self.day 
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json'     
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
            return True
        else:
            print "filenotfound "+filename
            return False
        
    def getJsonHeuristicMonth(self):
        if len(self.month) < 2:
            self.month = "0"+self.month     
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '.json'     
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
            return True
        else:
            print "filenotfound "+filename
            return False
        
    def getJsonHeuristicYear(self):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '.json'     
        if os.path.isfile(filename):
            print "getting file: "+filename
            f = open(filename, 'r')
            self.json = f.read()
            f.close()
            return True
        else:
            print "filenotfound "+filename
            return False
        
    def genEmptyTemplate(self):
        self.Entropy = defaultdict(int)
        self.Keywords = []
        self.jAnalytics = []
        self.jHeuristics = []
        self.jAbstracted = ""
        self.jMaster = defaultdict(int)
        self.jAnalytics = None
        
    def genGlobalJson(self):
        self.jAnalytics = { 
            "title": "impresa",
            "lang": "esp",
            "content" : self.jYears
        }
    
    def genMonthlyJSON(self):
        self.jAnalytics = { 
            "title": "impresa",
            "date": self.month+"/"+self.year,
            "incidence" : self.jMaster,
            "oddity" : self.Entropy,
            "keywords": self.Keywords,
            "content" : self.jHeuristics,
            "abstracted" : self.jAbstracted
        }
        
    def genYearlyJSON(self):
        self.jAnalytics = { 
            "title": "impresa",
            "date": self.year,
            "incidence" : self.jMaster,
            "oddity" : self.Entropy,
            "keywords": self.Keywords,
            "content" : self.jHeuristics,
            "abstracted" : self.jAbstracted
        }
            
         
    def nothingfound(self):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_NAME_PRINTED + self.year + '_' + self.month + '_' + self.day + '.json' 
        jOmNews = { 
           "title": const.DELIVERY_DESCRIPTION_PRINTED,
           "publication": const.PUB_NAME,
           "company": const.COMPANY_NAME,
           "message": "No se ha encontrado la fecha seleccionada",
           "debug": filename,
           "status" : "noresults"
           }
        
        self.result = json.dumps(jOmNews)
            
    def runRequest(self):
        mjson = json.loads(self.json,'utf-8')
        oddity =  mjson["oddity"]
        incidence =  mjson["incidence"]
        abstracted = mjson["abstracted"]
        heur = Heuristics('esp')
        heur._appendCompetitiveToMaster(2, self.Entropy, oddity)
        heur._appendAdditiveToMaster(2, self.jMaster, incidence)
        #self.jAbstracted += "|" + abstracted
        keywordlst = []
        for word in self.jMaster.keys():
            heur._appendWordToList(word, keywordlst)
        for word in self.Entropy.keys():
            heur._appendWordToList(word, keywordlst)
        self.Keywords = keywordlst   
        
    def getLoadedJsonKeywords(self):
        if self.json != None:
            try:
                mjson = json.loads(self.json,'utf-8')
                keywords =  mjson["keywords"]
                self.json = None
                return keywords
            except:
                return False
        else:
            return False
        
    def getLoadedDayJsonComputedKeywords(self):
        if self.json != None:
            try:
                mjson = json.loads(self.json,'utf-8')
                oddity =  mjson["oddity"]
                incidence = mjson["incidence"]
                keywords = []
                heur = Heuristics('esp')
                for word in oddity.keys():
                    heur._appendWordToList(word, keywords)
                for word in incidence.keys():
                    heur._appendWordToList(word, keywords)
                #self.json = None
                return keywords
            except:
                return False
        else:
            return False
        
    def _getLoadedDayJsonNoteKeywordBranch(self, dict):
        heur = Heuristics('esp')
        if self.json != None:
                mjson = json.loads(self.json,'utf-8')
                content =  mjson["content"]  
                for i in content:
                    for k,v in i.iteritems():
                        keywords = []
                        oddity =  v["oddity"]
                        incidence = v["incidence"]
                        heur = Heuristics('esp')
                        for word,num in oddity.iteritems():
                            if num>2:
                                heur._appendWordToList(word, keywords)
                        for word,num in incidence.iteritems():
                            if num>2:
                                heur._appendWordToList(word, keywords)
                        keywords = heur.makeAbstractList(keywords)
                        dict[k] = keywords
                self.json = None
        else:
            return False
             
    def dumpJsonMonthlyHeuristics(self):
        j =  json.dumps(self.jAnalytics, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '_' + self.month + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def dumpJsonYearlyHeuristics(self):
        j =  json.dumps(self.jAnalytics, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' + const.SAVING_HEURISTICS_NAME_PRINTED + self.year + '.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def dumpJsonGobalHeuristics(self):
        j =  json.dumps(self.jAnalytics, True, True, False, False, None, 3, None, 'utf-8', None, sort_keys=False)
        filename = const.SAVING_ROUTE + '/' + 'index.json'
        f = open(filename, 'w')
        f.write(j)
        f.close()
        
    def globalJsonIndexation(self):
        self.jYears = defaultdict(int)
        for y in range (2011,2013):
            self.year = str(y)
            self.getJsonHeuristicYear()
            jMonths = defaultdict(int)
            for m in range (1,13):
                self.month = str(m)
                self.getJsonHeuristicMonth()
                jDays = defaultdict(int)
                for d in range (1,32):
                    self.day = str(d)
                    self.getJsonHeuristicDay()
                    jNotes = defaultdict(int)
                    self._getLoadedDayJsonNoteKeywordBranch(jNotes)
                    if jNotes:
                        jDays[self.day] = jNotes
                if jDays:  
                    jMonths[self.month] = jDays
            if jMonths:
                self.jYears[self.year] = jMonths
        self.genGlobalJson()
        self.dumpJsonGobalHeuristics()   

    
                 
if __name__ == '__main__':
    #q = Indexation("year", year="2010")
    #r = Indexation("year", year="2011")
    #s = Indexation("year", year="2012")
    Indexation("global")
    
    
            
            

 

     
        
        