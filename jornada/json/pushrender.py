# -*- coding: utf-8 -*-


import sys, os
from compiler.ast import TryExcept

path_to = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
sys.path.append(path_to('../../'))

import logging
import httplib
import json
import constants as const
from datetime import datetime
import urllib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import smtplib



class PushRender(object):
    
    def __init__(self): 
        logging.getLogger().setLevel(logging.INFO)
        self.updates = []      
        self.html = ""
            
    def getPushCurrentHistory(self):
        path = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + 'current_history.json'             
        if os.path.isfile(path):
            f = open(path, 'r')
            jsontxt = f.read()
            f.close()
            try:
                return json.loads(jsontxt,'utf-8')
            except:
                logging.debug("history json error"+ path)
        else:
            logging.debug("history filenotfound "+ path)
            return  
        
    def renderCurrentPushHtml(self):
        json = self.getPushCurrentHistory()
        page = self.getTemplate('page')
        content = ""
        if json is not None:
            for item in json:
                fragment = self.getTemplate("item")
                fragment = fragment.replace('%TEXT%', item['text'])
                fragment = fragment.replace('%DATE%', item['time'][:-7])
                fragment = fragment.replace('%LINK%', item['link'],2)
                content += fragment
        else:
            content = self.getTemplate('empty')
        page = page.replace("%CONTENT%",content)
        return page
            
    def getResult(self):
        return self.result
    
    def getTemplate(self, template):
        return {
            'page':u'''
                    <html>
                    <head>
                    <title>Reporte de Notificaciones. La Jornada</title>
                    <style>
                        BODY { background: #222222; }
                        .main { 
                            font-family: 100% Arial, FreeSans, sans-serif; 
                            background: #FAFAFA; max-width: 800px; margin: 0 auto; padding-top:1em; padding-bottom:1em;
                        }
                        .info { margin: 1em; padding: 0.5em;}
                        .element { margin: 1em; padding: 0.5em; background: #F8F8F8; border: solid 1pt rgb(202, 23, 13); }
                        H3 { color: #205c90; margin:0; }
                        A { color: #C81B1B !important }
                    </style>
                    </head>
                    <body>
                    <div class="main">
                    <img src="http://www.jornada.unam.mx/ultimas/++theme++lajornada.portal.theme/imagenes/logo_jornada.png">
                    <div class="info">
                    <h1>Reporte de últimos 7 días de notificaciones.</h1>
                    </div>
                    %CONTENT%
                    </div>
                    </body>
                    </html>
                    ''',
            'item':u'<div class="element"><h3>%TEXT%</h3><i><b>%DATE%</b></i><br><b><a href="%LINK%">%LINK%</a></b></div>',
            'empty':u'<div class="element warning">No se han encontrado elementos</div>'    
            }.get(template, '')
    
    def saveText(self, name, content):
        pathname = const.SAVING_ROUTE + '/' + const.SAVING_NAME_CURRENT + name
        f = open(pathname, 'w')
        f.write(content)
        f.close()
        
    def sendMail(self, sender, recipients, html, plain):
        logging.info("sending mail...")
        login, password = 'movil@jornada.com.mx', 'b0n_cu3np4r4&m0v1l'
        server = 'smtp.jornada.com.mx'
        # create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header('subject…', 'utf-8')
        msg['From'] = login
        msg['To'] = recipients
        part1 = MIMEText(plain, 'plain', 'utf-8')
        part2 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        s = smtplib.SMTP_SSL(server, 465)
        #s = smtplib.SMTP(server)
        s.set_debuglevel(0)
        try:
            s.login(login, password)
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            logging.info("sent mail")
        except Exception, e:
            logging.info("error sending %s" % str(e))
        finally:
            logging.info("error sending")
            s.quit()
    

                      
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    sender = "movil@jornada.com.mx"
    recipients = ["lsjcp@yahoo.com, luis.j.camargo@gmail.com"]
    plain = 'void'
    html = PushRender().renderCurrentPushHtml()
    PushRender().saveText("pushreport.html", html)
    PushRender().sendMail(sender, recipients, html, plain)
    logging.info("saved pushreport.html")
    
 

     
        
        
