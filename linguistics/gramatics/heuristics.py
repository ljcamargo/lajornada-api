# -*- coding: utf-8 -*-
'''
Created on 19/06/2012

@author: lcammx
'''
import re
from linguistics.gramatics.esp import ESP as LANG

class Heuristics(object):
    
    def __init__(self, lang):
        self.lang = lang
        pass
  
    
    #POINTER
    
    def _processAbstraction(self, text, list):
        words = text.split()
        for word in words:
            self._appendWordToAbstractedString(word, list)
            
    def _matchDictToList(self, dict, list):
        dictkeys = dict.keys()
        for key in dictkeys:
            self._appendProcessedWordToList(key, list)
    
    def _matchArrayToList(self, textl, list):
            for text in textl:
                self._matchTextToList(text, list)
            
    def _matchTextToList(self, text, list):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;]','',text)
        words = text.split()
        for word in words:
            self._appendWordToList(word, list)            
    
    def _matchArrayToDict(self, textl, dict):
        for text in textl:
            self._matchTextToDict(text, dict)
        
    def _matchTextToDict(self, text, dict):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;]','',text)
        words = text.split()
        for word in words:
            self._appendWordToFreqDict(word, dict)

    def _proccessOddness(self, text, dict):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;]','',text)
        words = text.split()
        for word in words:
            self._calcWordOddness(word, dict)
    
    
    def _appendWordToList(self, text, list):
        isIn = False
        for litem in list:
            if litem == text: 
                isIn = True
        if not isIn:
            lang = LANG()
            if lang.isNounOrVerb(text):
                list.append(text)
                
    def _appendProcessedWordToList(self, text, list):
        isIn = False
        for litem in list:
            if litem == text: 
                isIn = True
        if not isIn:
            list.append(text)    
    
    def _appendWordToFreqDict(self, text, dict):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;]','',text)
        if dict.has_key(text):
            dict[text] += 1
        else:
            lang = LANG()
            if lang.isNounOrVerb(text):
                dict[text] = 1
    
    def _calcWordOddness(self, text, dict):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;]','',text)
        if dict.has_key(text):
            pass
        else:
            lang = LANG()
            dict[text] = lang.wordOddnessScore(text)
    
    
    def _appendWordToAbstractedString(self, text, list):
        lang = LANG()
        cat = lang.abstractCategory(text)
        if len(cat)>0:
            text = cat
        else:
            text = text.lower()
            text = lang.preProcess(text)
            text = lang.abstractToPhonetics(text)
            text = lang.collapseRedundant(text)
            text = lang.condenseSyllabs(text)
            text = lang.condenseDipthonge(text)
            list.append(text)
        
    def makeAbstractList(self, list):
        lang = LANG()
        nlist = []
        for text in list:
            cat = lang.abstractCategory(text)
            if len(cat)>0:
                text = cat
            else:
                text = text.lower()
                text = lang.preProcess(text)
                text = lang.abstractToPhonetics(text)
                text = lang.collapseRedundant(text)
                text = lang.condenseSyllabs(text)
                text = lang.condenseDipthonge(text)
            nlist.append(text)
        return nlist
    
    def makeKeywordAbstractList(self, list):
        lang = LANG()
        nlist = []
        for text in list:
            cat = lang.abstractCategory(text)
            if len(cat)>0:
                #text = cat
                pass
            else:
                text = text.lower()
                text = lang.preProcess(text)
                text = lang.abstractTo1stLevelPhonetics(text)
                nlist.append(text)
        return nlist
        
    def getAbstractedString(self, text):
        lang = LANG()
        cat = lang.abstractCategory(text)
        if len(cat)>0:
            text = cat
        else:
            text = text.lower()
            text = lang.preProcess(text)
            text = lang.abstractToPhonetics(text)
            text = lang.collapseRedundant(text)
            text = lang.condenseSyllabs(text)
            text = lang.condenseDipthonge(text)
        list.append(text)
    
    def selectHigherKeywords(self, infra, dict):
        for k,v in dict.iteritems():
            if v<infra:
                del dict[k]
        return dict
    
    def appendToMaster(self, infra, master, dict):
        for k,v in dict.iteritems():
            if v>infra:
                if master.has_key(k):
                    master[k] += v
                else:
                    master[k] = v
        return master
    
    def _appendAdditiveToMaster(self, infra, master, dict):
        for k,v in dict.iteritems():
            if v>infra:
                if master.has_key(k):
                    master[k] += v
                else:
                    master[k] = v
                    
    def _appendCompetitiveToMaster(self, infra, master, dict):
        for k,v in dict.iteritems():
            if v>infra:
                if master.has_key(k):
                    nv = v if v>master[k] else master[k]
                    master[k] = nv
                else:
                    master[k] = v
    
    def stripWordEnclousureMarks(self, word):
        list = "()[]{}'\""
        for c in list:
            word = word.replace(c,"")
        return word
    
    def findProbableAdjacent(self,master,infra, circa, environ):
        for k,v in master.iteritems():
            if v>infra:
                for k2,v2, in master.iteritems():
                    if not k==k2:
                        if (abs(v2-v))<=circa:
                            partial = self.checkIfAdjacentInLists(k, k2, environ)
                            if partial>0:
                                print "mix: "+k+":"+str(v)+" "+k2+":"+str(v2)+" scored:"+str(partial)
                            
    def checkIfAdjacentInLists(self, word, guess, environ):
        score = 0
        for item in environ:
            for k,v in item.iteritems():
                values = v["words"]
                partial = self.isAdjacentInList(word, guess, values)
                if partial>0:
                    score +=partial
        return score
              
    def isAdjacentInList(self, word, guess, wlist):
        score = 0
        for i, val in enumerate(wlist):
            if val.decode('utf-8')==word.decode('utf-8'):
                if i<(len(wlist)-1):
                    if wlist[i+1].decode('utf-8')==guess.decode('utf-8'):
                        score +=1
        return score
                    

if __name__ == '__main__':
    pass