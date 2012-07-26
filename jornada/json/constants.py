# -*- coding: utf-8 -*-
'''
Created on 13/06/2012

@author: lcammx
'''

import os
path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))

SAVING_ROUTE = path_to('../../var')
SAVING_NAME_PRINTED = 'jornada_impresa_'
SAVING_NAME_CURRENT = 'jornada_ultimas_'
SAVING_ERROR_NAME_PRINTED = 'error_impresa_'
SAVING_ERROR_NAME_CURRENT = 'error_impresa_'
SAVING_HEURISTICS_NAME_PRINTED = 'heuristics_impresa_'
SAVING_HEURISTICS_NAME_CURRENT = 'heuristics_ultimas_'
ERROR_TITLE_PRINTED = u"Log Errores Noticias Impresas Periódico La Jornada"
ERROR_TITLE_CURRENT = u"Log Errores Últimas Noticias Periódico La Jornada"
ERROR_ALIAS = "error_impresa"
COMPANY_NAME = u"Demos Desarrollo de Medios S.A. de C.V."
PUB_NAME = u"La Jornada"
PUB_WEB = "http://www.jornada.unam.mx/"
PUB_ISBN = ""
PUB_PERIODICITY_PRINTED = "daily"
PUB_PERIODICITY_CURRENT = "hourly"
PUB_SCOPE = "news"
PUB_GENTIME_PRINTED = "05:00"
PUB_GENTIME_CURRENT = "+01:00"
DELIVERY_DESCRIPTION_PRINTED = u"Noticias Impresas Periódico La Jornada"
DELIVERY_DESCRIPTION_CURRENT = u"Últimas Noticias Periódico La Jornada"
DELIVERY_DESCRIPTION_UPDATES = u"Actualizaciones del Momento La Jornada"
DELIVERY_ALIAS_PRINTED = "lajornada_impresa"
DELIVERY_ALIAS_CURRENT = "lajornada_ultimas"
DELIVERY_ALIAS_UPDATES = "lajornada_updates"
DELIVERY_KIND_PRINTED = "impresa"
DELIVERY_KIND_CURRENT = "ultimas"
DELIVERY_KIND_UPDATES = "updates"
LOCALE_TIMEZONE = "GMT-6"
LOCALE_COUNTRY = u"México"
LOCALE_REGION = u"DF"
LOCALE_LANG = "ES"
LOCALE_CULTURE = "MX"
LOCALE_ENCODING = "UTF-8"
CONFIG_IMGSIZE = "1024x1024"
CONFIG_SNAPSIZE = "480x480"

