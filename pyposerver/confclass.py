import ConfigParser

class config:
    _conf = ""
    _filename = ""
    def __init__(self,filename):
        self._filename = filename
        self._conf = ConfigParser.ConfigParser()
        self._conf.read(self._filename)
    def getItems(self,value):
        return dict(self._conf.items(value))
    def getValue(self,section,item):
        return self._conf.get(section,item)
    def getMulValue(self,itembuf):
        retValue = []
        count = len(itembuf)
        for item in itembuf:
            tmp = self._conf.get(item[0],item[1])
            retValue.append(tmp)
        return retValue
    def setValue(self,section,item,value):
        ret = True
        try:
            self._conf.set(section,item,value)
            self._conf.write(open(self._filename,'w'))
        except Error as msg:
            print msg
            ret = False
        return ret
    def setMulValue(self,bufvalue):
        ret = True
        ilen = len(bufvalue)
        try:
            for item in bufvalue:
                self._conf.set(item[0],item[1],item[2])
            self._conf.write(open(self._filename,'w'))
        except Error as msg:
            print msg
            ret = False
        return ret
