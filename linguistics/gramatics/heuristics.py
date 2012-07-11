'''
Created on 19/06/2012

@author: lcammx
'''

from collections import defaultdict
from linguistics.gramatics.esp import ESP as LANG

class Heuristics(object):
    
    def __init__(self, lang):
        self.lang = lang
        pass
  
    
    #POINTER
    
    def _matchArrayToList(self, textl, list):
            for text in textl:
                self._matchTextToList(text, list)
            
    def _matchTextToList(self, text, list):
        words = text.split()
        for word in words:
            self._appendWordToList(word, list)
    
    def _matchArrayToDict(self, textl, dict):
        for text in textl:
            self._matchTextToDict(text, dict)
        
    def _matchTextToDict(self, text, dict):
        words = text.split()
        for word in words:
            self._appendWordToFreqDict(word, dict)

    def _proccessOddness(self, text, dict):
        words = text.split()
        for word in words:
            self._calcWordOddness(word, dict)
    
    
    def _appendWordToList(self, text, list):
        text = text.replace("(","")
        text = text.replace(")","")
        isIn = False
        for litem in list:
            if litem == text: 
                isIn = True
        if not isIn:
            lang = LANG()
            if lang.isNounOrVerb(text):
                list.append(text)  
    
    def _appendWordToFreqDict(self, text, dict):
        text = text.replace("(","")
        text = text.replace(")","")
        if dict.has_key(text):
            dict[text] += 1
        else:
            lang = LANG()
            if lang.isNounOrVerb(text):
                dict[text] = 1
    
    def _calcWordOddness(self, text, dict):
        if dict.has_key(text):
            pass
        else:
            lang = LANG()
            dict[text] = lang.wordOddnessScore(text)
    
    
    
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