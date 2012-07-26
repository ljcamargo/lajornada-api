'''
Created on 14/06/2012

@author: lcammx
'''

import sys, os
path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../'))

from jornada.json.api import Api
from cgi import parse_qs, escape

def application(environ, start_response):
    status = '200 OK'        
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    family = escape(parameters['family'][0]) if 'family' in parameters else ""
    section = escape(parameters['section'][0]) if 'section' in parameters else ""
    mtype = escape(parameters['type'][0]) if 'type' in parameters else ""
    noteid = escape(parameters['id'][0]) if 'id' in parameters else ""
    txt = escape(parameters['search'][0]) if 'search' in parameters else ""
    year = escape(parameters['year'][0]) if 'year' in parameters else ""
    month = escape(parameters['month'][0]) if 'month' in parameters else ""
    day = escape(parameters['day'][0]) if 'day' in parameters else ""
    detail = escape(parameters['detail'][0]) if 'detail' in parameters else ""
    richness = escape(parameters['richness'][0]) if 'richness' in parameters else ""
	soruce = escape(parameters['source'][0]) if 'source' in parameters else ""
    thisapi = Api(family,section,mtype,txt,noteid,year,month,day,detail, richness, source)
    output = thisapi.getResult()
    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
