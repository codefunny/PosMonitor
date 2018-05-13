# -*- coding: cp936 -*-
import time
import random
import sqlite3
import pyDes
import binascii as ba

def getDate():
    datestr = time.strftime("%m%d",time.localtime())
    return datestr
def getTime():
    timestr = time.strftime("%H%M%S",time.localtime())
    return timestr

def chMkeyPara(conf):
    oldMk = conf.getValue("mkey","mk")
    print "TMK : %s\n"%oldMk
    
    newMk = raw_input("请输入新的TMK：")
    if newMk == "" or newMk.isspace():
        newMk = oldMk
    elif len(newMk)!=32 or newMk.isalnum() != True:
        print "输入的密钥成分需为数字和字母"
        return
    
    conf.setValue("mkey","mk",newMk)
    print("now TMK：%s"%newMk)

    return

def showallssn(posdb,sqlite3):
    conn = sqlite3.connect(posdb)
    cur = conn.cursor()
    cur.execute("select * from posdata")
    res = cur.fetchall()

    print "-"*117
    print "| %3s | %4s | %12s | %6s | %12s | %7s | %7s | %8s | %7s | %8s | %8s |"%\
          ("id","mti","amt","ssn","rrn","batcode","authcode","respcode","msgtype","trantime","trandate")
    for v in res:
            print "| %3s | %4s | %12s | %6s | %12s | %7s | %7s  | %8s | %7s | %8s | %8s |"%\
                  (v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10])
    cur.close()
    conn.close()
    print "-"*117

    return

"""查找一条记录"""
def selectOne(posdb,sqlite3,indata):
    ret = True
    msgtype = indata[0]
    ossnstr = indata[1]
    batcodestr = indata[2]
    
    conn = sqlite3.connect(posdb)
    cur = conn.cursor()
    try:
        cur.execute("select * from posdata where ssn='%s' and batcode='%s' and msgtype='%s'"%(ossnstr,batcodestr,msgtype))
    except sqlite3.Error as e:
        print(e)
        cur.close()
        conn.close()	
        ret = False
        return ret

    ret = cur.fetchone()	
    cur.close()
    conn.close()
    
    return ret

"""查找最后一笔交易"""
def selectLastTran(posdb,sqlite3,indata):
    ret = True
    print indata
    msgtype = indata[0]
    mtistr = indata[1]
    batcodestr = indata[2]
    
    conn = sqlite3.connect(posdb)
    cur = conn.cursor()
    sqldata = "select * from posdata where mti='%s' and batcode='%s' and msgtype='%s' order by ssn desc limit 1 offset 0"%\
              (mtistr,batcodestr,msgtype)
    try:
        cur.execute(sqldata)
    except sqlite3.Error as e:
        print(e)
        cur.close()
        conn.close()	
        ret = False
        return ret

    ret = cur.fetchone()	
    cur.close()
    conn.close()
    
    return ret

"""插入一条数据到数据库"""
def insertOneData(posdb,sqlite3,indata):
    creattable = "create table if not exists posdata(id integer primary key autoincrement,mti varchar(5),\
amt varchar(13),ssn varchar(7),rrn varchar(13),batcode varchar(7),authcode varchar(7),respcode varchar(3),\
msgtype varchar(5),trantime varchar(7),trandate varchar(5))"
    ret = True
    conn = sqlite3.connect(posdb)
    cur = conn.cursor()
    #cur.execute("drop table posdata")
    cur.execute(creattable)
    sqldata = "insert into posdata(mti,amt,ssn,rrn,batcode,authcode,respcode,msgtype,trantime,trandate) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%\
                (indata[0],indata[1],indata[2],indata[3],indata[4],indata[5],indata[6],indata[7],indata[8],indata[9])
    try:
        cur.execute(sqldata)
    except sqlite3.Error as e:
        print(e)
        cur.close()
        conn.close()	
        ret = False
        return ret
                 
    conn.commit()
    cur.close()
    conn.close()
    return ret

def delallssn(posdb,sqlite3):
    conn = sqlite3.connect(posdb)
    cur = conn.cursor()
    cur.execute("delete from posdata")
    conn.commit()
    cur.close()
    conn.close()
    print("delete ok")

    return

"""查找商户号"""
def selectOneMerc(dbfile,sqlfd,indata):
    ret = True
    mercode = indata

    sqldata = "select * from merchant where code='%s'"
    sqldata %=mercode
    conn = sqlfd.connect(dbfile)
    cur = conn.cursor()
    try:
        cur.execute(sqldata)
    except sqlfd.Error as e:
        print(e)
        cur.close()
        conn.close()	
        ret = False
        return ret

    ret = cur.fetchone()	
    cur.close()
    conn.close()
    
    return ret

"""查找终端主密钥"""
def selectTmk(dbfile,sqlfd,indata):
    ret = True
    termcode = indata[0]
    mercode = indata[1]

    sqldata = "select master_key,bat_code,sett_date from term where code='%s' and mer_code='%s'"
    sqldata %=termcode,mercode
    conn = sqlfd.connect(dbfile)
    cur = conn.cursor()
    try:
        cur.execute(sqldata)
    except sqlfd.Error as e:
        print(e)
        cur.close()
        conn.close()	
        ret = False
        return ret

    ret = cur.fetchone()	
    cur.close()
    conn.close()
    
    return ret

def getWorkKey(count):
    listNum = "1234567890ABCDEF1234567890ABCDEF"
    key = ""
    for i in xrange(count):
        index = random.randint(0,31)
        key += listNum[index]

    return key

"""根据inItems进行打包"""
def doPackTrans(iso,inItems,head):
    if head != '':
        iso.setHead(head)
    if inItems[0][0] != 0:
        return False
    iso.setMTI(inItems[0][1])
    for item in inItems[1:]:
        if item[1] != "":
            iso.setBit(item[0],item[1])
    return True


def recvTrans(isoRcv,sysbit37,sysbit38):
    tranItems = ''
    mtistr = isoRcv.getMTI()
    print 'MTI : %s'%mtistr
    v1 = isoRcv.getBitsAndValues()
    for v in v1:
        print('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))

    if mtistr == '0800':
        print("签到响应")
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit32 = ""
        bit62 = ""

        indata = bit42
        ret = selectOneMerc("dbms.db",sqlite3,indata)
        if ret == False or ret == None:
            print "找不到这样的商户号"
            bit39 = "03"
        else:
            bit32 = ret[3].encode('utf-8')
            indata = [bit41,bit42]
            ret = selectTmk("dbms.db",sqlite3,indata)
            if ret == False or ret == None:
                print "找不到这样的终端号"
                bit39 = "97"
            else:
                k1 = ret[0].encode('utf-8').strip()
                #k1 = "1073E6190825D37029C4A838EA80C43B"
                pinkey = getWorkKey(32)
                mackey = getWorkKey(16)
                print pinkey,mackey
                k = pyDes.triple_des(ba.a2b_hex(k1))
                pinkey = k.encrypt(ba.a2b_hex(pinkey))
                mackey = k.encrypt(ba.a2b_hex(mackey))
                pinkey = ba.b2a_hex(pinkey)
                mackey = ba.b2a_hex(mackey)
                mackey = mackey.ljust(32,'0')
                print("%s,%s"%(pinkey,mackey))
                h62 = pinkey+"00000000"
                l62 = mackey+"00000000"
                bit62 = h62+l62
                bit39 = "00"
            
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit37 = sysbit37
        bit60 = isoRcv.BITMAP_VALUES[60]
        tranItems = [[0,"0810"],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [32,bit32],\
                     [37,bit37],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [60,bit60],\
                     [62,bit62],\
                     [64,'1111111111111111']]
        
    elif mtistr == '0200' and isoRcv.BITMAP_VALUES[3] == '000000' and isoRcv.BITMAP_VALUES[25] == '00':
        print("消费响应")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit60 = isoRcv.BITMAP_VALUES[60]
        tranItems = [[0,"0210"],\
                     [2,bit2],\
                     [3,'000000'],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'00'],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]


    elif mtistr == '0400' and isoRcv.BITMAP_VALUES[3] == '000000' and isoRcv.BITMAP_VALUES[25] == '00':
        print("消费冲正")
        bit2 = "4340617200411561"
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit60 = isoRcv.BITMAP_VALUES[60]
        tranItems = [[0,"0410"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'00'],\
                     [32,bit32],\
                     [37,bit37],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [60,bit60],\
                     [64,'1111111111111111']]

    elif mtistr == '0200' and isoRcv.BITMAP_VALUES[3] == '200000' and isoRcv.BITMAP_VALUES[25] == '00':
        print("消费撤销")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0210"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'00'],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [60,bit60],\
                     [61,bit61],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]
        
    elif mtistr == '0220' and isoRcv.BITMAP_VALUES[3] == '200000' and isoRcv.BITMAP_VALUES[25] == '00':
        print("退货")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0230"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'00'],\
                     [32,bit32],\
                     [37,bit37],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]

    elif mtistr == '0200' and isoRcv.BITMAP_VALUES[3] == '310000' and isoRcv.BITMAP_VALUES[25] == '00':
        print("查询")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit54 = "0201156C000000001234"
        bit60 = isoRcv.BITMAP_VALUES[60]
        tranItems = [[0,"0230"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'00'],\
                     [32,bit32],\
                     [37,bit37],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [54,bit54],\
                     [60,bit60],\
                     [64,'1111111111111111']]
        
    elif mtistr == '0100' and isoRcv.BITMAP_VALUES[3] == '030000' and isoRcv.BITMAP_VALUES[25] == '06':
        print("预授权")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0110"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [23," "],\
                     [25,'06'],\
                     [32,bit32],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]
                      
    elif mtistr == '0100' and isoRcv.BITMAP_VALUES[3] == '200000' and isoRcv.BITMAP_VALUES[25] == '06':
        print("预授权撤销")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0110"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [23," "],\
                     [25,'06'],\
                     [32,bit32],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]
                      
    elif mtistr == '0200' and isoRcv.BITMAP_VALUES[3] == '000000' and isoRcv.BITMAP_VALUES[25] == '06':
        print("预授权完成")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0210"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'06'],\
                     [32,bit32],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]


    elif mtistr == '0200' and isoRcv.BITMAP_VALUES[3] == '200000' and isoRcv.BITMAP_VALUES[25] == '06':
        print("预授权完成撤销")
        bit2 = (isoRcv.BITMAP_VALUES[35])[:16]
        bit3 = isoRcv.BITMAP_VALUES[3]
        bit4 = isoRcv.BITMAP_VALUES[4]
        bit11 = isoRcv.BITMAP_VALUES[11]
        bit12 = getTime()
        bit13 = getDate()
        bit15 = bit13
        bit32 = "00000088"
        bit37 = sysbit37
        bit38 = sysbit38
        bit39 = "00"
        bit41 = isoRcv.BITMAP_VALUES[41]
        bit42 = isoRcv.BITMAP_VALUES[42]
        bit44 = "00010000   00000011   "
        bit53 = isoRcv.BITMAP_VALUES[53]
        bit60 = isoRcv.BITMAP_VALUES[60]
        bit61 = isoRcv.BITMAP_VALUES[61]
        tranItems = [[0,"0110"],\
                     [2,bit2],\
                     [3,bit3],\
                     [4,bit4],\
                     [11,bit11],\
                     [12,bit12],\
                     [13,bit13],\
                     [14,"9999"],\
                     [15,bit15],\
                     [25,'06'],\
                     [32,bit32],\
                     [37,bit37],\
                     [38,bit38],\
                     [39,bit39],\
                     [41,bit41],\
                     [42,bit42],\
                     [44,bit44],\
                     [49,'156'],\
                     [53,bit53],\
                     [60,bit60],\
                     [63,"CUP"],\
                     [64,'1111111111111111']]
                      
    else:
        print("The server dosen't understand my message!")

    return tranItems
