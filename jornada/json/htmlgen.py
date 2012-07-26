'''
Created on 25/07/2012

@author: lcammx
'''

import re

class HTMLgen(object):

    

    def __init__(self, coding):
        self.coding = coding

    
    def genArticle(self, article):
        html = "<html><head>"
        header = "<title>"+article['title']+"</title></head>"
        body = "<body>"
        title = "<h1>"+article['title']+"</h1>"
        byline = "<p class=\"byline\">"+article['byline']+"</p>"
        hedline = "<p class=\"hedline\">"+article['hedline']+"</p>"
        image = "<img class=\"article\" src=\""+article['imgurl']+"\"/><br/>"
        content = "<p class=\"content\">"+article['content']+"</p>"
        end = "</body></html>"
        r = html + header + body + title + byline + hedline + image + content + end
        return r 
    
    def sanHTML(self, text):
        text =  re.sub("<[\/]{0,1}(hl1|hl2|firstp|div|span)[^><]*>", "", text)
        #text =  re.sub("<\s*media-reference[^>]*>(.*?)<\s*/\s*media-reference>", "", text)
        #text =  re.sub("<\s*media-caption[^>]*>(.*?)<\s*/\s*media-caption>", "", text)
        #text =  re.sub("<\s*media-producer[^>]*>(.*?)<\s*/\s*media-producer>", "", text)
        text =  re.sub("<\s*media.*?>(.*?)<\s*\/\s*media\s*.*?>", "", text)
        return text
     