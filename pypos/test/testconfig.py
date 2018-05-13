#!/usr/bin/python 

import ConfigParser

print "1","32"
def getMulValue(conf,inbuf):
    retValue = []
    count = len(inbuf)
    print inbuf[0][0],inbuf[0][1]
    print inbuf[1][0],inbuf[1][1]
    for item in inbuf:
        tmpValue = conf.get(item[0],item[1])
        retValue.append(tmpValue)
    return retValue

config = ConfigParser.ConfigParser()
config.read("isoconfig.ini")

sections = config.sections()

print sections

options = config.options("main")
print options

items = config.items("main")
print items

items1 = dict(config.items("main"))
print items1
print items1["tpdu"]

context = config.get("main","TPDU")
print context

items = [["main","tid"],["main","mid"]]

count = getMulValue(config,items)
print count


    
