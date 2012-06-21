'''
Created on 18/06/2012

@author: lcammx
'''
import re

class Language(object):

    def __init__(self):
        #GRAMMAR CATEGORIES
        self.articles = {  
            u"determinate" : { u"el", u"la", u"los", u"las" },
            u"undeterminate" : { u"un", u"unos", u"una", u"unas" }                          
            }
        self.adjetives = {  
            u"posesive" : { u"mi", u"mis", u"tu", u"tus", u"su", u"sus", u"nuestro", u"nuestros", u"nuestra", u"nuestras", u"vuestro", u"vuestros", u"vuestra", u"vuestras" },
            u"undeterminate" : { u"un", u"unos", u"una", u"unas" }                          
            }
        self.prepositions = {
            u"formal" : { u"a", u"ante", u"bajo", u"cabe", u"con", u"contra", u"de", u"desde", u"en", u"entre", u"hacia", u"hasta", u"para", u"por", u"según", u"sin", u"so", u"sobre", u"tras" },
            u"value" : { u"durante", u"mediante", u"excepto", u"salvo", u"incluso", u"más", u"menos" },
            u"phrasal" : { }                
            }
        self.adverbs = {
            u"place" : { u"aquí", u"allí", u"ahí", u"allá", u"acá", u"arriba", u"abajo", u"cerca", u"lejos", u"delante", u"detrás", u"encima", u"debajo", u"enfrente", u"atrás", u"alrededor" },
            u"time" : { u"pronto", u"tarde", u"temprano", u"todavía", u"aún", u"ya", u"ayer", u"hoy", u"mañana", u"siempre", u"nunca", u"jamás", u"próximamente", u"prontamente", u"anoche", u"enseguida", u"ahora", u"mientras", u"antier" },  
            u"mode" : { u"bien", u"mal", u"regular", u"despacio", u"deprisa", u"así", u"tal", u"como", u"aprisa", u"adrede", u"peor", u"mejor", u"$mente" },          
            u"grade" : { u"muy", u"poco", u"muy poco", u"mucho", u"bastante", u"más", u"menos", u"algo", u"demasiado", u"casi", u"sólo", u"solamente", u"tan", u"tanto", u"todo", u"nada" },
            u"afirmation" : { u"sí", u"también", u"cierto", u"ciertamente", u"efectivamente", u"claro", u"exacto", u"obvio", u"verdaderamente", u"seguramente" },
            u"negation" : { u"no", u"jamás", u"nunca", u"tampoco", u"negativamente" },
            u"doubt" : { u"quizá", u"quizá", u"acaso", u"probablemente", u"posiblemente", u"seguramente", u"tal vez", u"sin duda", u"puede", u"puede ser", u"a lo mejor" }, 
            u"interrogative_exc" :  { u"cuándo", u"cómo", u"cuánto", u"dónde" },
            u"interrogative_rel" :  { u"cuando", u"como", u"cuanto", u"donde" },
            u"others" : { u"sólo", u"solamente", u"aun", u"inclusive", u"además", u"únicamente", u"incluso", u"mismamente", u"propiamente", u"precisamente", u"concretamente; viceversa", u"contrariamente", u"siquiera", u"consecuentemente" },         
        }
        self.conjuntions = {
             u"coordinant" : { u"y", u"e", u"o", u"u", u"pero", u"sino" },
             u"copulative" : { u"y", u"e", u"ni", u"que"},
             u"consecutive" : { u"con que", u"luego", u"tan", u"tanto que", u"así que", u"por lo tanto" },
             u"adversative" : { u"sin embargo", u"pero", u"con todo", u"a pesar de", u"no obstante", u"más bien", u"excepto", u"salvo", u"menos" },
             u"exclusive" : { u"sino", u"sino que", u"antes bien", u"al contrario" },
             u"disyuntives" : { u"o", u"u" },
             u"explicative" : { u"osea", u"esto es", u"es decir", u"mejor dicho", u"es más" }
             }
        self.pronouns = {
             u"tonic" : { u"yo", u"tú", u"vos", u"usted", u"él", u"ella", u"ello", u"nosotros", u"nosotras", u"ustedes", u"vosotros", u"vosotras", u"ellos", u"ellas" },
             u"tonic_prepositional" : { u"mi", u"conmigo", u"tí", u"contigo", u"sí", u"consigo" },
             u"atonic_sing" : { u"me", u"te", u"se", u"lo", u"la", u"le", u"se" },
             u"atonic_plural" : { u"nos", u"os", u"se", u"lo", u"la", u"les", u"los" },
             u"reflexive": { u"me", u"nos", u"te", u"os", u"se"},
             u"posesive" : { u"mío", u"mía", u"míos", u"mías", u"tuyo", u"tuya", u"tuyos", u"tuyas", u"suyo", u"suya", u"suyos", u"suyas", u"nuestro", u"nuestra", u"nuestros", u"nuestras", u"vuestro", u"vuestra", u"vuestros", u"vuestras"  },
             u"posesive" : { u"mío", u"mía", u"míos", u"mías", u"tuyo", u"tuya", u"tuyos", u"tuyas", u"suyo", u"suya", u"suyos", u"suyas", u"nuestro", u"nuestra", u"nuestros", u"nuestras", u"vuestro", u"vuestra", u"vuestros", u"vuestras"  },
             u"demostrative" : { u"éste", u"ésta", u"esto", u"éstos", u"éstas", u"ése", u"ésa", u"eso", u"ésos", u"ésas", u"aquel", u"aquella", u"aquello", u"aquéllos", u"aquéllas"   },
             u"relative" : { u"que", u"cual", u"cuales", u"donde", u"quien", u"quienes", u"cuyo", u"cuya", u"cuyos", u"cuyas" },
             u"numeral" : { u"doble", u"triple", u"cuádruple" }
             }
        self.other = { 
              u"synthagmal": { u"al", u"del" },
              u"logic" : { u"si" },
              u"lownum" : { u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15"}
              }
        self.commonverbs = {
            u"estar" : { u"estar", u"estando", u"estado", u"estoy", u"estás", u"está", u"estamos", u"están", u"esta", u"estáis", 
                        u"estuve", u"estuviste", u"estuvo", u"estuvimos", u"estuvieron", u"estuvísteis", 
                        u"estaré", u"estarás", u"estará", u"estaremos", u"estarán", u"estaréis",
                        u"estaba", u"estabas", u"estaba", u"estábamos", u"estaban", u"estábais",
                        u"estaría", u"estarías", u"estaría", u"estaríamos", u"estarían", u"estaríais",
                        u"esté", u"estés","esté", u"estemos", u"estén", u"estéis",
                        u"estuviera", u"estuvieras", u"estuviera", u"estuviéramos", u"estuvieran", u"estuviérais", 
                        u"estuviese", u"estuvieses", u"estuviese", u"estuviésemos", u"estuviesen", u"estuviéseis",
                        u"estuviere", u"estuvieres", u"estuvieres", u"estuviéremos", u"estuvieren", u"estuviéreis"
                        },
            u"ser" : { u"ser", u"siendo", u"sido", u"soy", u"eres", u"es", u"somos", u"son", u"sois"
                      u"fuí", u"fuiste", u"fué", u"fuimos", u"fueron", u"fuísteis",
                      u"seré", u"serás", u"será", u"seremos", u"serán", u"seréis",
                      u"era", u"eras", u"era", u"éramos", u"eran", u"érais",
                      u"sería", u"serías", u"sería", u"seríamos", u"serían", u"seríais",
                      u"sea", u"seas", u"sea", u"seamos", u"sean", u"seais",
                      u"fuera","fueras", u"fuera", u"fuéramos", u"fueran", u"fuérais",
                      u"fuese", u"fueses","fuese", u"fuésemos", u"fuesen", u"fuéseis",
                      u"fuere", u"fueres", u"fuere", u"fuéremos", u"fuésen", u"fuéreis"                     
                     }
                                            
            }
        
            
    
    
    def isNounOrVerb(self, text):
        isNV = True
        text = text.lower()
        isNV = isNV and (not (self.isInCategory(self.other, text)))
        isNV = isNV and (not (self.isInCategory(self.adverbs, text)))
        isNV = isNV and (not (self.isInCategory(self.adjetives, text)))
        isNV = isNV and (not (self.isInCategory(self.articles, text)))
        isNV = isNV and (not (self.isInCategory(self.conjuntions, text)))
        isNV = isNV and (not (self.isInCategory(self.prepositions, text)))
        isNV = isNV and (not (self.isInCategory(self.pronouns, text)))
        isNV = isNV and (not (self.isInCategory(self.other, text)))
        isNV = isNV and (not (self.isInCategory(self.commonverbs, text)))
        return isNV
    
    def isInCategory(self, category, text):
        for k,v in category.iteritems():
            for word in v:
                if text == word.decode('utf-8'):
                    return True
        return False
        

    def languageEntropy(self, word):
        tautosilabs = {"pr", "br", "fr", "tr", "dr", "kr", "gr", "pl", "bl", "fl", "ti", "kl", "gl" }
        ends = "jxhut"
        starts = "xw"
        ccallowed = { "ll","rr", "cc", "ee","oo" }
        score = 0
        if len(word)>4: score +=1
        if len(word)>8: score +=1
        if (word!=word.lower()): score += 1
        word = word.lower()
        if (word!=self.voidchar(word, u'ñxwk')): score += 1
        if (word!=self.voidchar(word, u'jáéú')): score += 1
        if (word!=self.voidchar(word, u'!$%&/()?¡¿?*´')): score += 1
        if (self.hasCluster(word, tautosilabs)): score += 1
        if (self.hasStart(word, starts)): score += 1
        if (self.hasEnding(word, ends)): score += 1
        if (self.hasDouble(word, ccallowed)): score += 1
        print "entropy: "+word+" = "+str(score)
        return score
           
    
    def hasCluster(self, word, clusters):
        for cluster in clusters:
            if word.find(cluster):
                return True
        return False
    
    def voidchar(self, text, chars):
        for c in list(chars):
            text.replace(c,'')
        return text
    
    def hasEnding(self, text, chars):
        for c in list(chars):
            if c==text[-1]:
                return True
        return False   
    
    def hasStart(self, text, chars):
        for c in list(chars):
            if c==text[0]:
                return True
        return False
    
    def hasDouble(self, text, but):
        for i in range(len(text)-1):
            if text[i]==text[i+1]:
                dd = text[i:i+1]
                if dd in but:
                    return True
        return False
    
            
