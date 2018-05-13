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

"""消费、消费撤销、退货、预授权、预授权撤销、预授权完成、预授权完成撤销"""
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
        #修改终端参数
        outdata = []
        chTermPara(conf,outdata)
        mid = outdata[0]
        tid = outdata[1]
        tpdu = outdata[2]
        head = outdata[3]
    elif innum == 2:
        #通讯参数
        outdata = []
        chLinePara(conf,outdata)
        serverIP = outdata[0]
        serverPort = outdata[1]
    elif innum == 3:
        #终端密钥
        chMkeyPara(conf)
    elif innum == 4:
        #其他参数
        outdata = []
        chOtherPara(conf,outdata)
        lbatcode = outdata[0]
        lssn = outdata[1]
        timeBetweenEcho = outdata[2]
        numberEcho = outdata[3]
    elif innum == 5:
        #显示所有参数
        showconf(conf)
    elif innum == 6:
        #显示交易数据
        showallssn(posdb,sqlite3)
    elif innum == 7:
        #删除交易数据
        delallssn(posdb,sqlite3)
    
    return


for req in range(0,numberEcho):
    iso = ISO8583()
    tranItems = []
    
    tran_num = menu()
    if tran_num > 14 or tran_num <0 or tran_num == -1:
        continue
    
    if tran_num == 0:
        print "退出"
        break
    
    if tran_num == 5:
        print "管理"
        mngnum = mngmenu()
        if mngnum not in range(1,8):
            continue
        funcmng(mngnum)
        continue
    
    if tran_num == 1:
        print "签到"
        tranItems = [[0,"0800"],\
                     [11,lssn.zfill(6)],\
                     [41,tid],\
                     [42,mid],\
                     [60,"00000008003"],\
                     [63,"01 "]]
        
    elif tran_num == 2:
        print("消费交易")
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
                print "密码加密有误"
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
        print("消费撤销")
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
        print "退货"
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
        print "查询"
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
        print "消费冲正最后一笔"
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
        print "撤销冲正最后一笔"
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
        print("预授权")
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
                print "密码加密有误"
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
        print("预授权撤销")
        ret = checkPadData()
        if ret ==  False:
            continue

        datestr,authcode,amtstr = ret
        batcodestr = lbatcode

        bit11 = lssn.encode('utf-8').zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit38 = authcode
        bit60 = '11'+batcodestr+'000501'
        #bit61 = 原批次号+原流水号+交易日期
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
        print("预授权完成请求")
        ret = checkPadData()
        if ret ==  False:
            continue
        datestr,authcode,amtstr = ret
        batcodestr = lbatcode

        bit11 = lssn.encode('utf-8').zfill(6)
        bit35 = '4340617200411561d14071010000091900000'
        bit38 = authcode
        bit60 = '20'+lbatcode+'000501'
        #bit61 = 原批次号+原流水号+交易日期
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
        print("预授权完成撤销")
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
        #bit61 = 原批次号+原流水号+交易日期
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
        print("功能尚未实现")
        continue

    HEADER = tpdu + head
    ret = doPackTrans(iso,tranItems,HEADER)
    if ret == False:
        print "报文有问题 ：（"
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
		
