# -*- coding: utf-8 -*-
'''
Created on 13/05/2012

@author: lcammx
'''
from impresa import Impresa
import logging
               
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    for x in range(60,360):
        logging.info("minus %s" % str(x))
        print 
        try:
            Impresa(minus=x)
        except:
            logging.info("not found")