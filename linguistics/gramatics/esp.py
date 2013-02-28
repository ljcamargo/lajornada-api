# -*- coding: utf-8 -*-
'''
Created on 18/06/2012

@author: lcammx
'''

from language import Language
import re 

DEBUG = True

class ESP(Language):     
    tautosyllabs = (u'pr', u'br', u'fr', u'tr', u'dr', u'kr', u'gr', u'pl', u'bl', u'fl', u'ti', u'kl', u'gl')
    ends = u'jxhut'
    starts = u'xw'
    ccallowed = (u'll', u'rr', u'cc', u'ee', u'oo')
    categories = {
        'articles': {  
            'determinate':   (u'el', u'la', u'los', u'las'),
            'undeterminate': (u'un', u'unos', u'una', u'unas'),                          
        }, 
        'adjetives': {  
            'posesive':      (u'mi', u'mis', u'tu', u'tus', u'su', u'sus', u'nuestro', u'nuestros', u'nuestra', u'nuestras', u'vuestro', u'vuestros', u'vuestra', u'vuestras'),
            'undeterminate': (u'un', u'unos', u'una', u'unas'),                         
        },
        'prepositions': {
            'formal':  (u'a', u'ante', u'bajo', u'cabe', u'con', u'contra', u'de', u'desde', u'en', u'entre', u'hacia', u'hasta', u'para', u'por', u'según', u'sin', u'so', u'sobre', u'tras'),
            'value':   (u'durante', u'mediante', u'excepto', u'salvo', u'incluso', u'más', u'menos'),
            'phrasal': ()
        },       
        'adverbs': {
            'place':             (u'aquí', u'allí', u'ahí', u'allá', u'acá', u'arriba', u'abajo', u'cerca', u'lejos', u'delante', u'detrás', u'encima', u'debajo', u'enfrente', u'atrás', u'alrededor'),
            'time':              (u'pronto', u'tarde', u'temprano', u'todavía', u'aún', u'ya', u'ayer', u'hoy', u'mañana', u'siempre', u'nunca', u'jamás', u'próximamente', u'prontamente', u'anoche', u'enseguida', u'ahora', u'mientras', u'antier'),  
            'mode':              (u'bien', u'mal', u'regular', u'despacio', u'deprisa', u'así', u'tal', u'como', u'aprisa', u'adrede', u'peor', u'mejor', u'$mente'),          
            'grade':             (u'muy', u'poco', u'muy poco', u'mucho', u'bastante', u'más', u'menos', u'algo', u'demasiado', u'casi', u'sólo', u'solamente', u'tan', u'tanto', u'todo', u'nada'),
            'afirmation':        (u'sí', u'también', u'cierto', u'ciertamente', u'efectivamente', u'claro', u'exacto', u'obvio', u'verdaderamente', u'seguramente'),
            'negation':          (u'no', u'jamás', u'nunca', u'tampoco', u'negativamente'),
            'doubt':             (u'quizá', u'quizá', u'acaso', u'probablemente', u'posiblemente', u'seguramente', u'tal vez', u'sin duda', u'puede', u'puede ser', u'a lo mejor'), 
            'interrogative_exc': (u'cuándo', u'cómo', u'cuánto', u'dónde'),
            'interrogative_rel': (u'cuando', u'como', u'cuanto', u'donde'),
            'others':            (u'sólo', u'solamente', u'aun', u'inclusive', u'además', u'únicamente', u'incluso', u'mismamente', u'propiamente', u'precisamente', u'concretamente; viceversa', u'contrariamente', u'siquiera', u'consecuentemente'),         
        },     
        'conjuntions': {
            'coordinant':  (u'y', u'e', u'o', u'u', u'pero', u'sino'),
            'copulative':  (u'y', u'e', u'ni', u'que'),
            'consecutive': (u'con que', u'luego', u'tan', u'tanto que', u'así que', u'por lo tanto'),
            'adversative': (u'sin embargo', u'pero', u'con todo', u'a pesar de', u'no obstante', u'más bien', u'excepto', u'salvo', u'menos'),
            'exclusive':   (u'sino', u'sino que', u'antes bien', u'al contrario'),
            'disyuntives': (u'o', u'u'),
            'explicative': (u'osea', u'esto es', u'es decir', u'mejor dicho', u'es más'),
            'logic':      (u'si')
         },
         'pronouns': {
             'tonic':               (u'yo', u'tú', u'vos', u'usted', u'él', u'ella', u'ello', u'nosotros', u'nosotras', u'ustedes', u'vosotros', u'vosotras', u'ellos', u'ellas'),
             'tonic_prepositional': (u'mi', u'conmigo', u'tí', u'contigo', u'sí', u'consigo'),
             'atonic_sing':         (u'me', u'te', u'se', u'lo', u'la', u'le', u'se'),
             'atonic_plural':       (u'nos', u'os', u'se', u'lo', u'la', u'les', u'los'),
             'reflexive':           (u'me', u'nos', u'te', u'os', u'se'),
             'posesive':            (u'mío', u'mía', u'míos', u'mías', u'tuyo', u'tuya', u'tuyos', u'tuyas', u'suyo', u'suya', u'suyos', u'suyas', u'nuestro', u'nuestra', u'nuestros', u'nuestras', u'vuestro', u'vuestra', u'vuestros', u'vuestras'),
             'posesive':            (u'mío', u'mía', u'míos', u'mías', u'tuyo', u'tuya', u'tuyos', u'tuyas', u'suyo', u'suya', u'suyos', u'suyas', u'nuestro', u'nuestra', u'nuestros', u'nuestras', u'vuestro', u'vuestra', u'vuestros', u'vuestras'),
             'demostrative':        (u'ese',u'este',u'éste', u'ésta', u'esto', u'éstos', u'éstas', u'ése', u'ésa', u'eso', u'ésos', u'ésas', u'aquel', u'aquella', u'aquello', u'aquéllos', u'aquéllas'),
             'relative':            (u'que', u'cual', u'cuales', u'donde', u'quien', u'quienes', u'cuyo', u'cuya', u'cuyos', u'cuyas'),
             'numeral':             (u'doble', u'triple', u'cuádruple'),
         }, 
         'other': {
             'synthagmal': (u'al', u'del', u'porque','vez'),
             'lownum':     (u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10', u'11', u'12', u'13', u'14', u'15'),
         },         
         'commonverbs': {
             'estar': (u'estar', u'estando', u'estado', u'estoy', u'estás', u'está', u'estamos', u'están', u'esta', u'estáis', 
                       u'estuve', u'estuviste', u'estuvo', u'estuvimos', u'estuvieron', u'estuvísteis', 
                       u'estaré', u'estarás', u'estará', u'estaremos', u'estarán', u'estaréis',
                       u'estaba', u'estabas', u'estaba', u'estábamos', u'estaban', u'estábais',
                       u'estaría', u'estarías', u'estaría', u'estaríamos', u'estarían', u'estaríais',
                       u'esté', u'estés','esté', u'estemos', u'estén', u'estéis',
                       u'estuviera', u'estuvieras', u'estuviera', u'estuviéramos', u'estuvieran', u'estuviérais', 
                       u'estuviese', u'estuvieses', u'estuviese', u'estuviésemos', u'estuviesen', u'estuviéseis',
                       u'estuviere', u'estuvieres', u'estuvieres', u'estuviéremos', u'estuvieren', u'estuviéreis'),
             'ser':   (u'ser', u'siendo', u'sido', u'soy', u'eres', u'es', u'somos', u'son', u'sois',
                       u'fuí', u'fuiste', u'fué', u'fue',u'fuimos', u'fueron', u'fuísteis',
                       u'seré', u'serás', u'será', u'seremos', u'serán', u'seréis',
                       u'era', u'eras', u'era', u'éramos', u'eran', u'érais',
                       u'sería', u'serías', u'sería', u'seríamos', u'serían', u'seríais',
                       u'sea', u'seas', u'sea', u'seamos', u'sean', u'seais',
                       u'fuera','fueras', u'fuera', u'fuéramos', u'fueran', u'fuérais',
                       u'fuese', u'fueses','fuese', u'fuésemos', u'fuesen', u'fuéseis',
                       u'fuere', u'fueres', u'fuere', u'fuéremos', u'fuésen', u'fuéreis'),
             'haber': (u'haber',u'hay,'u'he',u'has',u'ha',u'hemos',u'han',
                       u'habré',u'habrás',u'habrá',u'habremos',u'habrán'),
             'decir': (u'decir',u'digo',u'dices',u'dice',u'decimos',u'dicen'
                       u'dije',u'dijiste',u'dijo',u'dijimos',u'dijeron',
                       u'diré',u'dirás',u'dirá',u'diremos',u'dirán'),
                         
         }                             
    }
    
    def wordOddnessScore(self, word):    
        word = u'%s' % word.strip(' ,.;-') 
        score = 0
        if len(word) > 4: score += 1
        if len(word) > 8: score += 1 
        if word != word.lower(): score += 1
        if re.search(r'[ñxwk]', word, re.IGNORECASE): score += 1
        if re.search(r'[jáéú]', word, re.IGNORECASE): score += 1
        if re.search(r'[!\$\%\&\/\(\)\?¡¿\?\*`]', word, re.IGNORECASE): score += 1
        if re.search(r'%s' % '|'.join(self.tautosyllabs), word, re.IGNORECASE): score += 1
        if re.search(r'^[%s]' % self.starts, word, re.IGNORECASE): score += 1
        if re.search(r'[%s]$' % self.ends, word, re.IGNORECASE): score += 1
        if re.search(r'([^%s])\1' % '|'.join(self.ccallowed), word, re.IGNORECASE): score += 1
        
        #if DEBUG: print u'entrpy: %s = %i' % (word, score) 
        
        return score
    
    def preSoftProcess(self, text):
        text = re.sub(u'[\(\)\[\]\'\"¿¡?!,;.]','',text)
        return text
    
    def preProcess(self, text):
        text = re.sub(u'[\(\)\[\]\'\"]','',text)
        text = re.sub(u'[?!]',',',text)
        text = re.sub(u'[¡¿]','',text)
        text = re.sub(u'[#$%&]','',text)
        text = re.sub('^\.', '', text)
        text = re.sub('^\-', '', text)
        text = re.sub('^\*', '', text)
        text = re.sub('^/', '', text)
        text = re.sub('^\.', '', text)
        text = re.sub('^"', '', text)
        text = re.sub('^\'', '', text)
        text = re.sub('^,', '', text)
        text = re.sub('\.$', '', text)
        text = re.sub('\-$', '', text)
        text = re.sub('/$', '', text)
        text = re.sub('\*$', '', text)
        text = re.sub(',$', '', text)
        text = re.sub('"$', '', text)
        text = re.sub('\'$', '', text)
        text = text.replace(u"\u2018","")
        text = text.replace(u"\u2019","")
        text = text.replace(u"\u201c","")
        text = text.replace(u"\u201d","")
        return text
    
    def abstractToPhonetics(self, text):
        text = text.replace(u"á","a")
        text = text.replace(u"é","e")
        text = text.replace(u"í","i")
        text = text.replace(u"ó","o")
        text = text.replace(u"ú","u")
        text = text.replace(u"h","")
        text = text.replace(u"ll","y")
        text = text.replace(u"qu","c")
        text = text.replace(u"gu","j")
        text = text.replace(u"gü","ju")
        text = re.sub(u'[mnñ]','m',text)
        text = re.sub(u'[bdpt]','b',text)
        text = re.sub(u'[ckqg]','m',text)
        text = re.sub(u'[szyx]','s',text)
        text = re.sub(u'[iuw]','i',text)
        text = re.sub(u'[1234567890]','0',text)
        return text
    
    def abstractTo1stLevelPhonetics(self, text):
        text = text.replace(u"á","a")
        text = text.replace(u"é","e")
        text = text.replace(u"í","i")
        text = text.replace(u"ó","o")
        text = text.replace(u"ú","u")
        text = text.replace(u"ñ","n")
        text = text.replace(u"ü","u")
        return text
    
    def collapseRedundant(self, text):
        text = text.replace(u"aa","a")
        text = text.replace(u"bb","b")
        text = text.replace(u"cc","c")
        text = text.replace(u"ee","e")
        text = text.replace(u"ff","f")
        text = text.replace(u"ii","i")
        text = text.replace(u"jj","j")
        text = text.replace(u"ll","l")
        text = text.replace(u"mm","m")
        text = text.replace(u"oo","o")
        text = text.replace(u"rr","r")
        text = text.replace(u"ss","s")
        text = text.replace(u"00","0")
        text = text.replace(u"baba","ba")
        text = text.replace(u"bebe","be")
        text = text.replace(u"bibi","bi")
        text = text.replace(u"bobo","bo")
        text = text.replace(u"mama","ma")
        text = text.replace(u"meme","me")
        text = text.replace(u"mimi","mi")
        text = text.replace(u"momo","mo")
        text = text.replace(u"caca","ca")
        text = text.replace(u"cece","ce")
        text = text.replace(u"cici","ci")
        text = text.replace(u"coco","co")
        text = text.replace(u"sasa","sa")
        text = text.replace(u"sese","se")
        text = text.replace(u"sisi","si")
        text = text.replace(u"soso","so")
        text = text.replace(u"rara","ra")
        text = text.replace(u"rere","re")
        text = text.replace(u"riri","ri")
        text = text.replace(u"roro","ro")
        text = text.replace(u"lala","la")
        text = text.replace(u"lele","le")
        text = text.replace(u"lili","li")
        text = text.replace(u"lolo","lo")
        text = text.replace(u"yaya","ya")
        text = text.replace(u"yeye","ye")
        text = text.replace(u"yiyi","yi")
        text = text.replace(u"yoyo","yo")
        text = text.replace(u"jaja","ja")
        text = text.replace(u"jeje","je")
        text = text.replace(u"jiji","ji")
        text = text.replace(u"jojo","jo")
        text = text.replace(u"fafa","fa")
        text = text.replace(u"fefe","fe")
        text = text.replace(u"fifi","fi")
        text = text.replace(u"fofo","fo")
        return text

    def condenseSyllabs(self, text):
        text = text.replace(u"ba","b")
        text = text.replace(u"be","B")
        text = text.replace(u"bi","v")
        text = text.replace(u"bo","V")
        text = text.replace(u"ma","m")
        text = text.replace(u"me","M")
        text = text.replace(u"mi","n")
        text = text.replace(u"mo","N")
        text = text.replace(u"ca","c")
        text = text.replace(u"ce","C")
        text = text.replace(u"ci","k")
        text = text.replace(u"co","K")
        text = text.replace(u"sa","s")
        text = text.replace(u"se","S")
        text = text.replace(u"si","z")
        text = text.replace(u"so","Z")
        text = text.replace(u"ra","r")
        text = text.replace(u"re","R")
        text = text.replace(u"ri","h")
        text = text.replace(u"ro","H")
        text = text.replace(u"la","l")
        text = text.replace(u"le","L")
        text = text.replace(u"li","d")
        text = text.replace(u"lo","D")
        text = text.replace(u"ya","y")
        text = text.replace(u"ye","Y")
        text = text.replace(u"yi","x")
        text = text.replace(u"yo","X")
        text = text.replace(u"ja","j")
        text = text.replace(u"je","J")
        text = text.replace(u"ji","t")
        text = text.replace(u"jo","T")
        text = text.replace(u"fa","f")
        text = text.replace(u"fe","F")
        text = text.replace(u"fi","w")
        text = text.replace(u"fo","W")
        return text
    
    def condenseDipthonge(self, text):
        text = text.replace(u"ia","A")
        text = text.replace(u"ie","E")
        text = text.replace(u"io","O")
        text = text.replace(u"ii","I")
        text = text.replace(u"aa","Á")
        text = text.replace(u"ae","É")
        text = text.replace(u"ai","Í")
        text = text.replace(u"ao","O")
        text = text.replace(u"ea","á")
        text = text.replace(u"ee","é")
        text = text.replace(u"ei","í")
        text = text.replace(u"eo","é")
        text = text.replace(u"oa","u")
        text = text.replace(u"oe","U")
        text = text.replace(u"ii","ú")
        text = text.replace(u"io","Ú")
        return text
        