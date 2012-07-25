# -*- coding: utf-8 -*-
'''
Created on 11/06/2012

@author: lcammx
'''

from api import Api  
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

     
class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            
            if urlparse(self.path).query:
                params = parse_qs(urlparse(self.path).query)
                family = params.get("family")[0] if params.has_key("family") else ""
                section = params.get("section")[0] if params.has_key("section") else ""
                mtype = params.get("type")[0] if params.has_key("type") else ""
                noteid = params.get("id")[0] if params.has_key("id") else ""
                txt = params.get("search")[0] if params.has_key("search") else ""
                year = params.get("year")[0] if params.has_key("year") else ""
                month = params.get("month")[0] if params.has_key("month") else ""
                day = params.get("day")[0] if params.has_key("day") else ""
                detail = params.get("detail")[0] if params.has_key("detail") else ""
                richness = params.get("richness")[0] if params.has_key("richness") else ""
                thisapi = Api(family,section,mtype,txt,noteid,year,month,day,detail,richness)
                #Application/json
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(thisapi.getResult())
            else:       
                thisapi = Api()
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(thisapi.getResult())
        except Exception as e:
            self.send_error(503,'Servicio No Disponible '+e.__str__())
            
            
            
def main():
    try:
        server = HTTPServer(('0.0.0.0', 1984), Server)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()       
                      
if __name__ == '__main__':
    main()
        
        
        