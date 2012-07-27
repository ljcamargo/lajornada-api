# -*- coding: utf-8 -*-

'''
Created on 26/07/2012

@author: lcammx
'''
import urllib, httplib
import jornada.json.constants as const
import json
import os

class NotificationsManager(object):

    def __init__(self):
        pass
        self.androidkey = const.KEY_ANDROID_API_PUSH
    
    def registerId(self, id, kind):
        print 'registering '+id
        List = self.getList(kind)
        if not id in List:
            List.append(id)
            self.saveList(List, kind)
        
    def unregId(self, id, kind):
        print 'unregistering '+id
        List = self.getList(kind)
        if id in List:
            List.remove(id)
            self.saveList(List, kind)
    
    def getList(self, name):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_PUSH_LIST + name + '.txt'
            
        if os.path.isfile(filename):
            print "getting file: " + filename
            f = open(filename, 'r')
            List = f.readlines()
            f.close() 
            return List
        else:
            return []
        
    
    def saveList(self, List, name):
        filename = const.SAVING_ROUTE + '/' + const.SAVING_PUSH_LIST + name + '.txt'
        f = open(filename, 'w')
        print 'Escribiendo archivo: %s' % filename
        for item in List:
            if not item == "" and not item == "\n":
                f.write(item)
                f.write('\n')
        f.close()
        

    
    def sendPushToUserList(self, kind, message, addendum):
        List = self.getList(kind)
        print List
        if len(List)>0 and not message == "":
            self.pushToAndroid(List, message, addendum)
        
    def pushToAndroid(self, List, message, addendum):
        request = {
              "data": {"message": message },
              "registration_ids": List
             }
        data = json.dumps(request)
        print "json sent to android"
        print data
        try:
            h = httplib.HTTPConnection('https://android.googleapis.com/gcm/send',5228)
            headers={'Content-Type': 'application/json','Authorization': self.androidkey}
            h.request('POST', '/', data, headers)
            r = h.getresponse()
            print "request to android:"
            print r.read()
        except Exception as e:
            print e.__str__()
            

    def pushToApple(self, List, message, addendum):
        Apple = {
            "aps": {
                "alert": message,
                "badge": 1,
                "sound": "default"       
                },
             "rel": {
                "url":addendum,
                "name": "La Jornada"
                }
        }
        print json.dumps(Apple)


