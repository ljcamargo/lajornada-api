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
    
    def abstractCategory(self, text):
        for category in self.categories.keys():
            if self.isInCategory(self.categories[category], text):
                if category == "articles": return "$"
                if category == "adjetives": return "$"
                if category == "pronouns": return "$"
                if category == "prepositions": return "#"
                if category == "adverbs": return "@"
                if category == "conjunctions": return "%"
                if category == "other": return "&"
                if category == "commonverbs": return "!"
        return ""
    
    def isInCategory(self, category, text): 
        text = text.lower().strip(' ,.;-')
        for subcat in category.values(): 
            for word in subcat: 
                if text == word:
                    return True
        return False        
        
        
        
    def wordOddnessScore(self, word):
        pass
