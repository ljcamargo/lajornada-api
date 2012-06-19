'''
Created on 13/05/2012

@author: lcammx
'''

class parsing(object):
    
    def __init__(self):
        '''constructor'''
            
    def dumpJsonItems(self, jItems):
        '''method'''
        
    def dumpErrorLog(self, error):
        '''method'''
    
    def getText(self, nodelist):
            rc = []
            try:
                mem = ""
                for node in nodelist: 
                    if node.nodeType == node.TEXT_NODE:
                        val = node.nodeValue
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace(): 
                                if len(val)<2: 
                                    mem = val
                                else:                                
                                    rc.append(mem+val)
                                    mem = ""
            except:
                rci = nodelist.nodeValue
                return rci
            str = ''.join(rc)
            return str.strip() 
        
    def getRecursiveText(self, nodelist):
            rc = []
            try:
                if nodelist.hasChildNodes():
                    for node in nodelist.childNodes: 
                        val = self.getRecursiveText(node)
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace():                              
                                rc.append(val)
                else:
                    if nodelist.nodeType == nodelist.TEXT_NODE:
                        val = self.getLastText(nodelist)                   
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace():                              
                                rc.append(val)
                    
            except Exception as e:
                rci = e.__str__()
                return rci
            return ''.join(rc)
        
    def getLastText(self, node):
            rc = ""
            try:
                val = node.nodeValue
                if val != None:
                    val = val.strip()
                    if val != "" and not val.isspace(): 
                        rc+=val                    
            except Exception as e:
                rci = e.__str__()
                return rci
            return rc
    
    def getArray(self, nodelist):
            rc = []
            try:
                mem = ""
                for node in nodelist: 
                    if node.hasChildNodes():
                        for nnode in node.childNodes:
                            val = self.getRecursiveText(nnode)
                            if val != None:
                                val = val.strip()
                                if val != "" and not val.isspace(): 
                                    if len(val)<2: 
                                        mem = val
                                    else:                                
                                        rc.append(mem+val)
                                        mem = ""
                    else:
                        val = node.nodeValue
                        if val != None:
                            val = val.strip()
                            if val != "" and not val.isspace(): 
                                if len(val)<2: 
                                    mem = val
                                else:                                
                                    rc.append(mem+val)
                                    mem = ""
                    
            except Exception as e:
                rci = e.__str__()
                return [rci]
            return rc


