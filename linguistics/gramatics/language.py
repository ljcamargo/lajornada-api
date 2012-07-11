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
    
    def wordOddnessScore(self, word):
        pass
