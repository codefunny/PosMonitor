# -*- coding: cp936 -*-
"""

(C) Copyright 2012 Steven.Zheng

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
import socket
import sys
import time
import binascii as ba
import inspect
import pyDes
from view import *
import sqlite3
import re
from function import *
from confclass import config
from debugstr import debugstring

class trans:
    def setLognTrans(self,tranbuf):pass
    def setTtfiTrans(self,tranbuf):pass
    def setTpayTrans(self,tranbuf):pass
    def setTrevTrans(self,tranbuf):pass
    def setTretTrans(self,tranbuf):pass
    def packTrans(self):pass
    def unpackTrans(self):pass           
    

creattable = "create table if not exists posdata(id integer primary key autoincrement,mti varchar(5),amt varchar(13),ssn varchar(7),rrn varchar(13),batcode varchar(7),respcode varchar(3),msgtype varchar(4))"
insertdata = "insert into table posdata(mti,amt,ssn,rrn,batcode,respcode,msgtype) values(?,?,?,?,?,?,?)"

conf = config("isoconfig.ini")
sitems = conf.getItems("server")
serverIP = sitems["ip"]
serverPort = sitems["port"]

baseitems = conf.getItems("lssn")
lssn = baseitems["localssn"]
lbatcode = baseitems["lbatcode"]
numberEcho = int(baseitems["numecho"])
timeBetweenEcho = int(baseitems["sleeptime"]) # in seconds

smain = conf.getItems("main")
tid = smain["tid"]
mid = smain["mid"]
tpdu = smain["tpdu"]
head = smain["head"]

spos = conf.getItems("posdb")
posdb = spos["dbname"]

"""���ѡ����ѳ������˻���Ԥ��Ȩ��Ԥ��Ȩ������Ԥ��Ȩ��ɡ�Ԥ��Ȩ��ɳ���"""
TRANTYPE = ("IPER","IPEV","IPET","IPAD","IPAV","IPCD","IPCV")

bigEndian = True
#bigEndian = False

s = None
	
def funcmng(innum):
    global mid,tid
    global serverIP,serverPort
    global lbatcode,lssn
    global timeBetweenEcho,numberEcho
    if innum == 1:
        #�޸��ն˲���
        outdata = []
        chTermPara(conf,outdata)
        mid = outdata[0]
        tid = outdata[1]
        tpdu = outdata[2]
        head = outdata[3]
    elif innum == 2:
        #ͨѶ����
        outdata = []
        chLinePara(conf,outdata)
        serverIP = outdata[0]
        serverPort = outdata[1]
    elif innum == 3:
        #�ն���Կ
        chMkeyPara(conf)
    elif innum == 4:
        #��������
        outdata = []
        chOtherPara(conf,outdata)
        lbatcode = outdata[0]
        lssn = outdata[1]
        timeBetweenEcho = outdata[2]
        numberEcho = outdata[3]
    elif innum == 5:
        #��ʾ���в���
        showconf(conf)
    elif innum == 6:
        #��ʾ��������
        showallssn(posdb,sqlite3)
    elif innum == 7:
        #ɾ����������
        delallssn(posdb,sqlite3)
    
    return


for req in range(0,numberEcho):
    iso = ISO8583()
    tranItems = []
    
    tran_num = menu()
    if tran_num > 14 or tran_num <0 or tran_num == -1:
        continue
    
    if tran_num == 0:
        print "�˳�"
        break
    
    if tran_num == 5:
        print "����"
        mngnum = mngmenu()
        if mngnum not in range(1,8):
            continue
        funcmng(mngnum)
        continue
    
    if tran_num == 1:
        print "ǩ��"
        tranItems = [[0,"0800"],\
                     [11,lssn.zfill(6)],\
                     [41,tid],\
                     [42,mid],\
                     [60,"00000008003"],\
                     [63,"01 "]]
        
    elif tran_num == 2:
        print("���ѽ���")
        ret = checkTpayData()
        if ret ==  False:
            continue
        amtstr,passwd = ret
        bit26=""
        bit52=""
        bit53="061"
        bit35 = '4340617200411561d14071010000091900000'
        if passwd == "":
            bit22 = "022"
        else:
            ret = getbit52(passwd,bit35,pyDes,ba)
            if ret == False:
                print "�����������"
                continue
            bit22 = "021"
            bit26="12"
            bit52 = ret
            bit53 = "261"
        
        bit60 = '22'+lbatcode.zfill(6)+'000501'
        tranItems = [[0,"0200"],\
                     [3,"000000"],\
                     [4,amtstr],\
                     [11,lssn.zfill(6)],\
                     [22,bit22],\
                     [25,"00"],\
                     [26,bit26],\
                     [35,bit35],\
                     [41,tid],\
                     [42,mid],\
                     [49,"156"],\
                     [52,bit52],\
                     [53,bit53+"0000000000000"],\
                     [60,bit60],\
                     [64,"1111111111111111"]]

    elif tran_num == 3:
        print("���ѳ���")
        ret = checkTrevData()
        if ret ==  False:
            continue
        msgtype = 'IPER'
        ossnstr = ret
        batcodestr = lbatcode
        indata = [msgtype,ossnstr,batcodestr]
        ret = selectOne(posdb,sqlite3,indata)
        if ret ==  False or ret == None:
            print "[ssn : %s,batcode : %s] errno:1403"%(ossnstr,batcodestr)
            continue
        res = ret

        bit11 = lssn.encode('utf-8').zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit37 = res[4].encode('utf-8').zfill(12)
        bit38 = res[6].encode('utf-8')
        bit61 = res[3].encode('utf-8').zfill(6) +ossnstr.zfill(6)
        tranItems = [[0,"0200"],\
                     [3,'200000'],\
                     [4,res[2].encode('utf-8')],\
                     [11,bit11],\
                     [22,'022'],\
                     [25,'00'],\
                     [35,bit35],\
                     [37,bit37],\
                     [38,bit38],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,'23'+lbatcode+'000501'],\
                     [61,bit61],\
                     [64,'1111111111111111']]
        
    elif tran_num == 4:
        print "�˻�"
        ret = checkRetData()
        if ret ==  False:
            continue
        bkamtstr,bkrrnstr,bkdatestr = ret
        bit35 = '4340617200411561d14071010000091900000'
        tranItems = [[0,"0220"],\
                     [3,'200000'],\
                     [4,bkamtstr],\
                     [11,lssn.zfill(6)],\
                     [22,'022'],\
                     [25,'00'],\
                     [35,bit35],\
                     [37,bkrrnstr],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,'25'+lbatcode+'000501'],\
                     [61,'000000000000'+bkdatestr],\
                     [63,'000'],\
                     [64,'1111111111111111']]

    elif tran_num == 6:
        print "��ѯ"
        bit35 = '4340617200411561d14071010000091900000'
        tranItems = [[0,"0200"],\
                     [3,'310000'],\
                     [11,lssn.zfill(6)],\
                     [22,'022'],\
                     [25,'00'],\
                     [35,bit35],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,'01'+lbatcode+'00050'],\
                     [64,'1111111111111111']]
        
    elif tran_num == 7:
        print "���ѳ������һ��"
        msgtype = 'IPER'
        mtistr = "0200"
        #ossnstr = str(int(lssn)-1)
        batcodestr = lbatcode
        indata = [msgtype,mtistr,batcodestr]
        ret = selectLastTran(posdb,sqlite3,indata)
        if ret ==  False or ret == None:
            print "[mit : %s,batcode : %s] errno:1403"%(mtistr,batcodestr)
            continue
        res = ret

        print res
        
        amtstr = res[2].encode('utf-8').zfill(12)
        ssnstr = res[3].encode('utf-8').zfill(6)
        #ssnstr = str(ossnstr).zfill(6)

        bit60 = '22'+lbatcode.zfill(6)+'000501'
        tranItems = [[0,"0400"],\
                     [3,"000000"],\
                     [4,amtstr],\
                     [11,ssnstr],\
                     [22,"022"],\
                     [25,"00"],\
                     [39,"06"],\
                     [41,tid],\
                     [42,mid],\
                     [49,"156"],\
                     [60,bit60],\
                     [64,"1111111111111111"]]
        
    elif tran_num == 8:
        print "�����������һ��"
        msgtype= 'IPEV'
        mtistr = "0200"
        batcodestr = lbatcode
        indata = [msgtype,mtistr,batcodestr]
        ret = selectLastTran(posdb,sqlite3,indata)
        if ret ==  False or ret == None:
            print "[mit : %s,batcode : %s] errno:1403"%(mtistr,batcodestr)
            continue
        res = ret

        amtstr = res[2].encode('utf-8').zfill(12)
        ssnstr = res[3].encode('utf-8').zfill(6)
        bit38 = res[6].encode('utf-8')
        bit60 = '23'+lbatcode+'000501'
        bit61 = res[5].encode('utf-8').zfill(6) +ssnstr
        tranItems = [[0,"0400"],\
                     [3,'200000'],\
                     [4,amtstr],\
                     [11,ssnstr],\
                     [22,'022'],\
                     [25,'00'],\
                     [38,bit38],\
                     [39,"06"],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [60,bit60],\
                     [61,bit61],\
                     [64,'1111111111111111']]
        
    elif tran_num == 9:
        print("Ԥ��Ȩ")
        ret = checkTpayData()
        if ret ==  False:
            continue
        amtstr,passwd = ret

        bit26=""
        bit52=""
        bit53="061"
        bit35 = '4340617200411561d14071010000091900000'
        if passwd == "":
            bit22 = "022"
        else:
            ret = getbit52(passwd,bit35,pyDes,ba)
            if ret == False:
                print "�����������"
                continue
            bit22 = "021"
            bit26="12"
            bit52 = ret
            bit53 = "261"
            
        bit60 = '10'+lbatcode.zfill(6)+'000501'
        tranItems = [[0,"0100"],\
                     [3,"030000"],\
                     [4,amtstr],\
                     [11,lssn.zfill(6)],\
                     [22,bit22],\
                     [25,"06"],\
                     [26,bit26],\
                     [35,bit35],\
                     [41,tid],\
                     [42,mid],\
                     [49,"156"],\
                     [52,bit52],\
                     [53,bit53+"0000000000000"],\
                     [60,bit60],\
                     [64,"1111111111111111"]]

    elif tran_num == 10:
        print("Ԥ��Ȩ����")
        ret = checkPadData()
        if ret ==  False:
            continue

        datestr,authcode,amtstr = ret
        batcodestr = lbatcode

        bit11 = lssn.encode('utf-8').zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit38 = authcode
        bit60 = '11'+batcodestr+'000501'
        #bit61 = ԭ���κ�+ԭ��ˮ��+��������
        bit61 = '000000000000'+datestr
        tranItems = [[0,"0100"],\
                     [3,'200000'],\
                     [4,amtstr],\
                     [11,bit11],\
                     [22,'022'],\
                     [25,'06'],\
                     [35,bit35],\
                     [38,bit38],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,bit60],\
                     [61,bit61],\
                     [64,'1111111111111111']]
        
    elif tran_num == 11:
        print("Ԥ��Ȩ�������")
        ret = checkPadData()
        if ret ==  False:
            continue
        datestr,authcode,amtstr = ret
        batcodestr = lbatcode

        bit11 = lssn.encode('utf-8').zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit38 = authcode
        bit60 = '20'+lbatcode+'000501'
        #bit61 = ԭ���κ�+ԭ��ˮ��+��������
        bit61 = '000000000000'+datestr
        tranItems = [[0,"0200"],\
                     [3,'000000'],\
                     [4,amtstr],\
                     [11,bit11],\
                     [22,'022'],\
                     [25,'06'],\
                     [35,bit35],\
                     [38,bit38],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,bit60],\
                     [61,bit61],\
                     [64,'1111111111111111']]

    elif tran_num == 12:
        print("Ԥ��Ȩ��ɳ���")
        ret = checkTrevData()
        if ret ==  False:
            continue
        msgtype = 'IPCD'
        ossnstr = ret
        batcodestr = lbatcode
        indata = [msgtype,ossnstr,batcodestr]
        ret = selectOne(posdb,sqlite3,indata)
        if ret ==  False or ret == None:
            print "[ssn : %s,batcode : %s] errno:1403"%(ossnstr,batcodestr)
            continue
        res = ret

        bit11 = lssn.zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit37 = res[4].encode('utf-8')
        bit38 = res[6].encode('utf-8')
        bit60 = '21' + lbatcode+'000501'
        #bit61 = ԭ���κ�+ԭ��ˮ��+��������
        bit61 = res[5].encode('utf-8') + ossnstr.zfill(6)+res[10].encode('utf-8')
        tranItems = [[0,"0200"],\
                     [3,'200000'],\
                     [4,amtstr],\
                     [11,bit11],\
                     [22,'022'],\
                     [25,'06'],\
                     [35,bit35],\
                     [37,bit37],\
                     [38,bit38],\
                     [41,tid],\
                     [42,mid],\
                     [49,'156'],\
                     [53,'0610000000000000'],\
                     [60,bit60],\
                     [61,bit61],\
                     [64,'1111111111111111']]
        
    elif tran_num == 13:
        print("������δʵ��")
        continue

    HEADER = tpdu + head
    ret = doPackTrans(iso,tranItems,HEADER)
    if ret == False:
        print "���������� ����"
        continue
        
    s = getsocket(socket,serverIP,serverPort)
    if s is None:
        print('Could not connect :(')
        continue
    
    try:
        message = iso.getNetworkISO()

        linenum = inspect.getframeinfo(inspect.currentframe())[1]
        debugstring(message,linenum,len(message))
        
        s.send(message)
        print('Sending ... %s' % str(message))
        try:
            s.settimeout(30)
            ans = s.recv(2048)
        except socket.timeout as e:
            s.close()
            print("timeout")
            continue
        except :
            continue
        print("\nIRecve Data")
        if len(ans) != 0:
            linenum = inspect.getframeinfo(inspect.currentframe())[1]
            debugstring(ans,linenum,len(ans))
        
        isoAns = ISO8583()
        try:
            isoAns.setNetworkISO(ans)
        except ISOError as msg:
            print msg
            continue
        
        recvTrans(iso,isoAns,conf,pyDes,posdb,sqlite3,ba,lbatcode,TRANTYPE)

    except ISOError as msg:
        print(msg)
        break

    lssn_tmp = int(lssn)+1
    lssn = str(lssn_tmp)
    print("lssn:"+lssn)
    time.sleep(timeBetweenEcho)
            
    if s is not None:
        s.close()

conf.setValue("lssn","localssn",lssn)	
		
print('Closing...')		
if s is not None:
    s.close()		
		
