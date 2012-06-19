'''
Created on 18/06/2012

@author: lcammx
'''

from language import Language

class ESP(Language):

    def __init__(self):
        #GRAMMAR CATEGORIES
        self.articles = {  
            "determinate" : { "el", "la", "los", "las" },
            "undeterminate" : { "un", "unos", "una", "unas" }                          
            }
        self.adjetives = {  
            "posesive" : { "mi", "mis", "tu", "tus", "su", "sus", "nuestro", "nuestros", "nuestra", "nuestras", "vuestro", "vuestros", "vuestra", "vuestras" },
            "undeterminate" : { "un", "unos", "una", "unas" }                          
            }
        self.prepositions = {
            "formal" : { "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre", "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras" },
            "value" : { "durante", "mediante", "excepto", "salvo", "incluso", "más", "menos" },
            "phrasal" : { }                
            }
        self.adverbs = {
            "place" : { "aquí", "allí", "ahí", "allá", "acá", "arriba", "abajo", "cerca", "lejos", "delante", "detrás", "encima", "debajo", "enfrente", "atrás", "alrededor" },
            "time" : { "pronto", "tarde", "temprano", "todavía", "aún", "ya", "ayer", "hoy", "mañana", "siempre", "nunca", "jamás", "próximamente", "prontamente", "anoche", "enseguida", "ahora", "mientras", "antier" },  
            "mode" : { "bien", "mal", "regular", "despacio", "deprisa", "así", "tal", "como", "aprisa", "adrede", "peor", "mejor", "$mente" },          
            "grade" : { "muy", "poco", "muy poco", "mucho", "bastante", "más", "menos", "algo", "demasiado", "casi", "sólo", "solamente", "tan", "tanto", "todo", "nada" },
            "afirmation" : { "sí", "también", "cierto", "ciertamente", "efectivamente", "claro", "exacto", "obvio", "verdaderamente", "seguramente" },
            "negation" : { "no", "jamás", "nunca", "tampoco", "negativamente" },
            "doubt" : { "quizá", "quizá", "acaso", "probablemente", "posiblemente", "seguramente", "tal vez", "sin duda", "puede", "puede ser", "a lo mejor" }, 
            "interrogative_exc" :  { "cuándo", "cómo", "cuánto", "dónde" },
            "interrogative_rel" :  { "cuando", "como", "cuanto", "donde" },
            "others" : { "sólo", "solamente", "aun", "inclusive", "además", "únicamente", "incluso", "mismamente", "propiamente", "precisamente", "concretamente; viceversa", "contrariamente", "siquiera", "consecuentemente" },         
        }
        self.conjuntions = {
             "coordinant" : { "y", "e", "o", "u", "pero", "sino" },
             "copulative" : { "y", "e", "ni", "que"},
             "consecutive" : { "con que", "luego", "tan", "tanto que", "así que", "por lo tanto" },
             "adversative" : { "sin embargo", "pero", "con todo", "a pesar de", "no obstante", "más bien", "excepto", "salvo", "menos" },
             "exclusive" : { "sino", "sino que", "antes bien", "al contrario" },
             "disyuntives" : { "o", "u" },
             "explicative" : { "osea", "esto es", "es decir", "mejor dicho", "es más" }
             }
        self.pronouns = {
             "tonic" : { "yo", "tú", "vos", "usted", "él", "ella", "ello", "nosotros", "nosotras", "ustedes", "vosotros", "vosotras", "ellos", "ellas" },
             "tonic_prepositional" : { "mi", "conmigo", "tí", "contigo", "sí", "consigo" },
             "atonic_sing" : { "me", "te", "se", "lo", "la", "le", "se" },
             "atonic_plural" : { "nos", "os", "se", "lo", "la", "les", "los" },
             "reflexive": { "me", "nos", "te", "os", "se"},
             "posesive" : { "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras"  },
             "posesive" : { "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras"  },
             "demostrative" : { "éste", "ésta", "esto", "éstos", "éstas", "ése", "ésa", "eso", "ésos", "ésas", "aquel", "aquella", "aquello", "aquéllos", "aquéllas"   },
             "relative" : { "que", "cual", "cuales", "donde", "quien", "quienes", "cuyo", "cuya", "cuyos", "cuyas" },
             "numeral" : { "doble", "triple", "cuádruple" }
             }
        self.other = { 
              "synthagmal": { "al", "del" },
              "logic" : { "si" },
              "lownum" : { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"}
              }
        self.commonverbs = {
            "estar" : { "estar", "estando", "estado", "estoy", "estás", "está", "estamos", "están", "esta", "estáis", 
                        "estuve", "estuviste", "estuvo", "estuvimos", "estuvieron", "estuvísteis", 
                        "estaré", "estarás", "estará", "estaremos", "estarán", "estaréis",
                        "estaba", "estabas", "estaba", "estábamos", "estaban", "estábais",
                        "estaría", "estarías", "estaría", "estaríamos", "estarían", "estaríais",
                        "esté", "estés","esté", "estemos", "estén", "estéis",
                        "estuviera", "estuvieras", "estuviera", "estuviéramos", "estuvieran", "estuviérais", 
                        "estuviese", "estuvieses", "estuviese", "estuviésemos", "estuviesen", "estuviéseis",
                        "estuviere", "estuvieres", "estuvieres", "estuviéremos", "estuvieren", "estuviéreis"
                        },
            "ser" : { "ser", "siendo", "sido", "soy", "eres", "es", "somos", "son", "sois"
                      "fuí", "fuiste", "fué", "fuimos", "fueron", "fuísteis",
                      "seré", "serás", "será", "seremos", "serán", "seréis",
                      "era", "eras", "era", "éramos", "eran", "érais",
                      "sería", "serías", "sería", "seríamos", "serían", "seríais",
                      "sea", "seas", "sea", "seamos", "sean", "seais",
                      "fuera","fueras", "fuera", "fuéramos", "fueran", "fuérais",
                      "fuese", "fueses","fuese", "fuésemos", "fuesen", "fuéseis",
                      "fuere", "fueres", "fuere", "fuéremos", "fuésen", "fuéreis"                     
                     }
                                            
            }

        