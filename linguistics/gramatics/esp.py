'''
Created on 18/06/2012

@author: lcammx
'''

from language import Language

class ESP(Language):     
    tautosilabs = (u'pr', u'br', u'fr', u'tr', u'dr', u'kr', u'gr', u'pl', u'bl', u'fl', u'ti', u'kl', u'gl')
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
         },
         'pronouns': {
             'tonic':               (u'yo', u'tú', u'vos', u'usted', u'él', u'ella', u'ello', u'nosotros', u'nosotras', u'ustedes', u'vosotros', u'vosotras', u'ellos', u'ellas'),
             'tonic_prepositional': (u'mi', u'conmigo', u'tí', u'contigo', u'sí', u'consigo'),
             'atonic_sing':         (u'me', u'te', u'se', u'lo', u'la', u'le', u'se'),
             'atonic_plural':       (u'nos', u'os', u'se', u'lo', u'la', u'les', u'los'),
             'reflexive':           (u'me', u'nos', u'te', u'os', u'se'),
             'posesive':            (u'mío', u'mía', u'míos', u'mías', u'tuyo', u'tuya', u'tuyos', u'tuyas', u'suyo', u'suya', u'suyos', u'suyas', u'nuestro', u'nuestra', u'nuestros', u'nuestras', u'vuestro', u'vuestra', u'vuestros', u'vuestras'),
             'posesive':            (u'mío', u'mía', u'míos', u'mías', u'tuyo', u'tuya', u'tuyos', u'tuyas', u'suyo', u'suya', u'suyos', u'suyas', u'nuestro', u'nuestra', u'nuestros', u'nuestras', u'vuestro', u'vuestra', u'vuestros', u'vuestras'),
             'demostrative':        (u'éste', u'ésta', u'esto', u'éstos', u'éstas', u'ése', u'ésa', u'eso', u'ésos', u'ésas', u'aquel', u'aquella', u'aquello', u'aquéllos', u'aquéllas'),
             'relative':            (u'que', u'cual', u'cuales', u'donde', u'quien', u'quienes', u'cuyo', u'cuya', u'cuyos', u'cuyas'),
             'numeral':             (u'doble', u'triple', u'cuádruple'),
         }, 
         'other': {
             'synthagmal': (u'al', u'del'),
             'logic':      (u'si',),
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
                       u'fuí', u'fuiste', u'fué', u'fuimos', u'fueron', u'fuísteis',
                       u'seré', u'serás', u'será', u'seremos', u'serán', u'seréis',
                       u'era', u'eras', u'era', u'éramos', u'eran', u'érais',
                       u'sería', u'serías', u'sería', u'seríamos', u'serían', u'seríais',
                       u'sea', u'seas', u'sea', u'seamos', u'sean', u'seais',
                       u'fuera','fueras', u'fuera', u'fuéramos', u'fueran', u'fuérais',
                       u'fuese', u'fueses','fuese', u'fuésemos', u'fuesen', u'fuéseis',
                       u'fuere', u'fueres', u'fuere', u'fuéremos', u'fuésen', u'fuéreis')
         }                             
    }

        