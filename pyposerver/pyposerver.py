"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
from socket import *
import inspect
from confclass import config
from debugstr import debugstring
from function import *

conf = config("sysconf.ini")
sitems = conf.getItems("sysconf")
sysbit37 = sitems["refcode"]
sysbit38 = sitems["authcode"]

# Configure the server
serverIP = "127.0.0.1" 
serverPort = 8583
maxConn = 5
bigEndian = True
#bigEndian = False


# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)    
# bind it to the server port
s.setblocking(True)
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind((serverIP, serverPort))   
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)                        


# Run forever
while 1:
        #wait new Client Connection
        connection, address = s.accept()
        while 1:
                # receive message
                isoStr = connection.recv(2048)
        
                if isoStr is None or len(isoStr) == 0:
                        break
                linenum = inspect.getframeinfo(inspect.currentframe())[1]
                debugstring(isoStr,linenum,len(isoStr))
                
                pack = ISO8583(debug=True)
                send = ISO8583()
                try:
                        pack.setNetworkISO(isoStr)

                        ret = recvTrans(pack,sysbit37,sysbit38)
                        if ret == "" or ret == None:
                                break
                        HEADER = "6000030000603100310120"
                        doPackTrans(send,ret,HEADER)

                        ans = send.getNetworkISO()
                except ISOError as msg:
                        print msg
                        break
                #except:
                #        print 'Something happened!!!!'
                #        break
                
                if ans is None or len(ans) == 0:
                        break
                linenum = inspect.getframeinfo(inspect.currentframe())[1]
                debugstring(ans,linenum,len(ans))

                connection.send(ans)

        #close socket
        connection.close()
        print "Closed..."
        sysbit37 = str(int(sysbit37)+1)
        sysbit38 = str(int(sysbit38)+1)
        conf.setValue("sysconf","refcode",sysbit37)
        conf.setValue("sysconf","authcode",sysbit38)	
                        
