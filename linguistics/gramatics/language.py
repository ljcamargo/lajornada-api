# -*- coding: utf-8 -*- #
'''
Created on 18/06/2012

@author: lcammx
'''
import re 
           
DEBUG = True

class Language(object):
    cateogories = dict()
    tautosilabs = list()
    ends = u''
    starts = u''
    ccallowed = list()
    
    def __init__(self):
        if not self.categories:
            raise NotImplementedError( "No language data")

    def isNounOrVerb(self, text):
        for category in self.categories.values():
            if self.isInCategory(category, text):
                return False 
        return True
    
    def isInCategory(self, category, text): 
        text = text.lower().strip(' ,.;-')
        for subcat in category.values(): 
            for word in subcat: 
                if text == word:
                    return True
        return False

    def languageEntropy(self, word):    
        word = u'%s' % word.strip(' ,.;-') 
        score = 0
        if len(word) > 4: score += 1
        if len(word) > 8: score += 1 
        if word != word.lower(): score += 1
        if re.search(r'[ñxwk]', word, re.IGNORECASE): score += 1
        if re.search(r'[jáéú]', word, re.IGNORECASE): score += 1
        if re.search(r'[!\$\%\&\/\(\)\?¡¿\?\*`]', word, re.IGNORECASE): score += 1
        if re.search(r'%s' % '|'.join(self.tautosilabs), word, re.IGNORECASE): score += 1
        if re.search(r'^[%s]' % self.starts, word, re.IGNORECASE): score += 1
        if re.search(r'[%s]$' % self.ends, word, re.IGNORECASE): score += 1
        if re.search(r'([^%s])\1' % '|'.join(self.ccallowed), word, re.IGNORECASE): score += 1
        
        if DEBUG: print u'entrpy: %s = %i' % (word, score) 
        
        return score