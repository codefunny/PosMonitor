# -*- coding: cp936 -*-

def chOtherPara(conf,outdata):
    items = conf.getItems("lssn")
    oldBat = items["lbatcode"]
    oldSsn = items["localssn"]
    oldTime = items["sleeptime"]
    oldEcho = items["numecho"]
    
    print "BatCode : %s"%oldBat
    print "LocSsn : %s"%oldSsn
    print "SleepTime : %s"%oldTime
    print "NumEcho : %s"%oldEcho

    newBat = raw_input("请输入新的批次号：")
    if newBat == "" or newBat.isspace():
        newBat = oldBat
    elif len(newBat) > 6 or newBat.isdigit() != True:
        print "输入的批次号必须为数字"
        return
    
    newSsn = raw_input("请输入新的流水号：")
    if newSsn == "" or newSsn.isspace():
        newSsn = oldSsn
    elif len(newSsn) > 6 or newSsn.isdigit() != True:
        print "输入的流水号必须为数字"
        return
    
    newTime = raw_input("请输入新的超时时间：")
    if newTime == "" or newTime.isspace():
        newTime = oldTime
    elif newTime.isdigit() != True:
        print "输入的超时时间必须为数字"
        return
    
    newEcho = raw_input("请输入新的周期数：")
    if newEcho == "" or newEcho.isspace():
        newEcho = oldEcho
    elif newEcho.isdigit() != True:
        print "输入的周期必须为数字"
        return
    
    newBat = newBat.zfill(6)
    newSsn = newSsn.zfill(6)
    outdata.append(newBat)
    outdata.append(newSsn)
    outdata.append(newTime)
    outdata.append(newEcho)
    newItems = [["lssn","lbatcode",newBat],\
                ["lssn","localssn",newSsn],\
                ["lssn","sleeptime",newTime],\
                ["lssn","numecho",newEcho]]
    conf.setMulValue(newItems)
    print("now BatCode：%s"%newBat)
    print("now LocalSsn：%s"%newSsn)
    print("now SleepTime：%s"%newTime)
    print("now NumEcho：%s"%newEcho)
    
    return

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

def chLinePara(conf,outdata):
    #pypos = re.compile(r"(((2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(((2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.)")
    items = conf.getItems("server")
    oldIp = items["ip"]
    oldPort = items["port"]
    print "IP : %s,PORT : %s\n"%(oldIp,oldPort)
    
    newIp = raw_input("请输入新的IP：")
    if newIp == "" or newIp.isspace():
        newIp = oldIp
    
    newPort = raw_input("请输入新的PORT：")
    if newPort == "" or newPort.isspace():
        newPort = oldPort

    outdata.append(newIp)
    outdata.append(newPort)
    newItems = [["server","ip",newIp],\
                ["server","port",newPort]]
    conf.setMulValue(newItems)
    print("now IP：%s"%newIp)
    print "now Port:%s"%newPort

    return

def chTermPara(conf,outdata):
    #global mid,tid
    items = conf.getItems("main")
    oldmid = items["mid"]
    oldtid = items["tid"]
    oldtpdu = items["tpdu"]
    oldhead = items["head"]
    print("原商户号：%s"%oldmid)
    print("原终端号：%s"%oldtid)
    print("原TPDU：%s"%oldtpdu)
    print("原报文头：%s"%oldhead)
    
    newmid = raw_input("请输入新商户号：")
    if newmid =="" or newmid.isspace():
            newmid = oldmid
    if len(newmid)!=15 or newmid.isalnum()!=True:
            print("商户号必须为15位,且为数字字母!")
            return

    newtid = raw_input("请输入新终端号：")
    if newtid =="" or newtid.isspace():
            newtid = oldtid
    if len(newtid)!=8 or newtid.isdigit()!=True:
            print("终端号必须为8位，且为数字！")
            return
        
    newtpdu = raw_input("请输入新TPDU：")
    if newtpdu =="" or newtpdu.isspace():
            newtpdu = oldtpdu
    if len(newtpdu)!=10 or newtpdu.isdigit()!=True:
            print("TPDU必须为10位，且为数字！")
            return
        
    newhead = raw_input("请输入新报文头：")
    if newhead =="" or newhead.isspace():
            newhead = oldhead
    if len(newhead)!=12 or newhead.isdigit()!=True:
            print("报文头必须为12位，且为数字！")
            return
        
    outdata.append(newmid)
    outdata.append(newtid)
    outdata.append(newtpdu)
    outdata.append(newhead)
    newItems = [["main","mid",newmid],["main","tid",newtid],
                ["main","tpdu",newtpdu],["main","head",newhead]]
    conf.setMulValue(newItems)
    print("新商户号：%s"%outdata[0])
    print("新终端号：%s"%outdata[1])
    print("新TPDU：%s"%outdata[2])
    print("新报文头：%s"%outdata[3])

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
    #cur.execute(creattable)
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

"""获取socket的fd"""
def getsocket(socket,serverIP,serverPort):
    for res in socket.getaddrinfo(serverIP, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            fd = socket.socket(af, socktype, proto)
        except socket.error as msg:
            fd = None
            continue
        try:
            fd.connect(sa)
        except socket.error as msg:
            fd.close()
            fd = None
            continue
        break
    return fd

"""根据inItems进行打包"""
def doPackTrans(iso,inItems,head):
    if head != '':
        iso.setHead(head)
    if inItems[0][0] != 0:
        return False
    iso.setMTI(inItems[0][1])
    for item in inItems[1:]:
        if item[1] !="":
            iso.setBit(item[0],item[1])
    return True

"""检查退货函数的输入参数"""
def checkRetData():
    ret = True
    errnum = 0
    bkamtstr = ""
    bkrrnstr = ""
    bkdatestr = ""
    
    while errnum < 3 :
        errnum += 1
        bkamt = raw_input("请输入金额：(如1200表示12元)")
        if bkamt == "" or bkamt.find('.') == True or len(bkamt)>12:
            print("输入金额有误！")
        else:
            bkamtstr = bkamt.zfill(12)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkrrn = raw_input("请输入原参考号：")
        if bkrrn == "" or bkrrn.isdigit() == False or len(bkrrn)>12:
            print("输入参考号有误！")
        else:
            bkrrnstr = bkrrn.zfill(12)
            break
        if errnum == 3:
            ret = False
            break

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkdate = raw_input("请输入日期：")
        if bkdate == "" or bkdate.isdigit() == False or len(bkdate)>4:
            print("输入日期有误！")
        else:
            bkdatestr = bkdate.zfill(4)
            break
        if errnum == 3:
            ret = False
            return ret
        
    return (bkamtstr,bkrrnstr,bkdatestr)

"""检查消费交易的输入参数"""
def checkTpayData():
    ret = True
    amtstr = ""
    errnum = 0
    while errnum < 3 :
        errnum += 1
        amt = raw_input("请输入金额：(如1200表示12元)")
        if amt == "" or amt.find('.') == True or len(amt)>12:
            print("输入金额有误！")
        else:
            amtstr = amt.zfill(12)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        passwd = raw_input("请输入密码：")
        if passwd != "" and len(passwd) != 6:
            print("密码长度固定为6位！")
        else:
            break

        if errnum == 3:
            ret = False
            return ret
 
    return amtstr,passwd

"""检查消费撤销的输入参数"""
def checkTrevData():
    ret = True
    ossnstr = ""
    errnum = 0
    while errnum < 3 :
        errnum += 1
        ossn = raw_input("请输入原凭证号：")
        if ossn == "" or ossn.isdigit() == False or len(ossn)>6:
            print("输入凭证号有误！")
        else:
            ossnstr = ossn.zfill(6)
            break
        if errnum == 3:
            ret = False
            return ret
    return ossnstr

"""检查预授权类参数"""
def checkPadData():
    ret = True
    errnum = 0
    bkamtstr = ""
    bkrrnstr = ""
    bkdatestr = ""

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkdate = raw_input("请输入日期：")
        if bkdate == "" or bkdate.isdigit() == False or len(bkdate)>4:
            print("输入日期有误！")
        else:
            bkdatestr = bkdate.zfill(4)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        authcode = raw_input("请输入授权号：")
        if authcode == "" or authcode.isdigit() == False or len(authcode)>6:
            print("输入授权号有误！")
        else:
            authcode = authcode.zfill(6)
            break
        if errnum == 3:
            ret = False
            break
        
    while errnum < 3 :
        errnum += 1
        bkamt = raw_input("请输入金额：(如1200表示12元)")
        if bkamt == "" or bkamt.find('.') == True or len(bkamt)>12:
            print("输入金额有误！")
        else:
            bkamtstr = bkamt.zfill(12)
            break
        if errnum == 3:
            ret = False
            return ret
        
    return (bkdatestr,authcode,bkamtstr)

def xorstr(str1,str2,ba):
    mlen = len(str2)
    xdata = list(str1)
                                                                           
    for j in range(0,8):                                                               
            tmp1 = ba.b2a_hex(xdata[j])                                          
            if j < mlen:                                                             
                    tmp2 = ba.b2a_hex(str2[j])                                 
                    tmp3 = "%x"%(int(tmp1,16) ^ int(tmp2,16))                          
            else:                                                                      
                    tmp3 = "%x"%(int(tmp1,16) ^ 0x00)                                  
            tmp3 = "%s"%tmp3                                                           
            tmp3 = tmp3.zfill(2)                                                       
            tmp4 = ba.a2b_hex(tmp3)                                              
            xdata[j] ="%s"% tmp4                                                                                
                                                                                     
    xdata1 = "".join(xdata)
    return ba.b2a_hex(xdata1)

def getbit52(inpwd,bit35,pyDes,ba):
    f1 = open("tpk.etc",'r')
    pinkey = f1.read()[:32]
    f1.close()

    if pinkey =="" or pinkey == None:
        return False
    
    inpwd = "06"+inpwd+"FFFFFFFF"
    tmp = (bit35.split("d")[0])[:-1]
    lindex = len(tmp)-12
    stror = "0000"+tmp[lindex:]
    
    inpwd = ba.a2b_hex(inpwd)
    stror = ba.a2b_hex(stror)
    passwd = xorstr(inpwd,stror,ba)
    
    k = pyDes.triple_des(ba.a2b_hex(pinkey))
    pindata = k.encrypt(ba.a2b_hex(passwd))
    bit52 = ba.b2a_hex(pindata)

    return bit52
            
def recvTrans(iso,isoAns,conf,pyDes,posdb,sqlite3,ba,lbatcode,TRANTYPE):
    mtistr = isoAns.getMTI()
    print 'MTI : %s'%mtistr
    v1 = isoAns.getBitsAndValues()
    for v in v1:
        print('Bit %s of type %s with value = [%s]' % (v['bit'],v['type'],v['value']))
    if mtistr == '0810':
        print("\tThat's great !!! The server understand my message !!!")
        if isoAns.BITMAP_VALUES[39] == '00':
            print("%s"% isoAns.getBit(62))
            value62 = isoAns.getBit(62)
            pinkey = value62[0:32]
            pinkey_check = value62[32:40]
            mackey = value62[40:56]
            mackey_check = value62[72:80]

            print("before decrypt\n pinkey:%s,pinkey_check:%s,\nmackey:%s,mackey_check:%s" \
                                %(pinkey,pinkey_check,mackey,mackey_check))
            k1 = conf.getValue("mkey","mk")
            k = pyDes.triple_des(ba.a2b_hex(k1))
            pinkey = k.decrypt(ba.a2b_hex(pinkey))
            mackey = k.decrypt(ba.a2b_hex(mackey))
            pinkey = ba.b2a_hex(pinkey)
            mackey = ba.b2a_hex(mackey)
            print("%s,%s"%(pinkey,mackey))

            #f1 = file("tpk.etc",'wr')
            f1 = open("tpk.etc",'w')
            f1.write(pinkey)
            f1.close()
            f2 = open("tmk.etc",'w');f2.write(mackey);f2.close()
            print("60:%s"%isoAns.getBit(60))
            batcode_tmp = isoAns.getBit(60)[2:8]
            lbatcode = batcode_tmp
            conf.setValue("lssn","localssn",lbatcode)
            print("batcode:%s"%lbatcode)
        else:
            print("logon false,[39]=%s"%isoAns.BITMAP_VALUES[39])
    elif mtistr == '0210' and v1[1]['value'] == '000000' and isoAns.BITMAP_VALUES[25] == '00':
        print("消费响应[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':         
            outdata = ['0200',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),isoAns.BITMAP_VALUES[37].zfill(12),\
                         lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],isoAns.BITMAP_VALUES[39],TRANTYPE[0],isoAns.BITMAP_VALUES[12],\
                       isoAns.BITMAP_VALUES[13]]     
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "插入数据库失败,xiaofei"
        else:
            print("xiaofei")
    elif mtistr == '0410' and v1[1]['value'] == '000000' and isoAns.BITMAP_VALUES[25] == '00':
        print("消费冲正[39]= %s"%isoAns.BITMAP_VALUES[39])
        """if isoAns.BITMAP_VALUES[39] == '00':
            conn = sqlite3.connect(posdb)
            cur = conn.cursor()
            #cur.execute("drop table posdata")
            #cur.execute(creattable)
            cur.execute("insert into posdata(mti,amt,ssn,rrn,batcode,respcode) values(%s,%s,%s,%s,%s,%s)"%\
                        ('0200',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),isoAns.BITMAP_VALUES[37].zfill(12),lbatcode.zfill(6),isoAns.BITMAP_VALUES[39]))
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("xiaofei")
        """
    elif mtistr == '0210' and v1[1]['value'] == '200000' and isoAns.BITMAP_VALUES[25] == '00':
        print("消费撤销[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':
            outdata = ['0200',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),\
                       isoAns.BITMAP_VALUES[37].zfill(12),lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],\
                       isoAns.BITMAP_VALUES[39],TRANTYPE[1],isoAns.BITMAP_VALUES[12],isoAns.BITMAP_VALUES[13]]
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "插入数据库失败"
        else:
            print("xiaofeichexiao")
    elif mtistr == '0230' and v1[1]['value'] == '200000' and isoAns.BITMAP_VALUES[25] == '00':
        print("退货[39]= %s"%isoAns.BITMAP_VALUES[39])
    elif mtistr == '0110' and v1[1]['value'] == '030000' and isoAns.BITMAP_VALUES[25] == '06':
        print("预授权[39]= %s"%isoAns.BITMAP_VALUES[39])
            
    elif mtistr == '0210' and v1[1]['value'] == '000000' and isoAns.BITMAP_VALUES[25] == '06':
        print("预授权完成[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':
            outdata = ['0100',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),\
                       isoAns.BITMAP_VALUES[37].zfill(12),lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],\
                       isoAns.BITMAP_VALUES[39],TRANTYPE[5],isoAns.BITMAP_VALUES[12],isoAns.BITMAP_VALUES[13]]
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "插入数据库失败"
        else:
            print("yushouquan")
    elif mtistr == '0210' and v1[1]['value'] == '200000' and isoAns.BITMAP_VALUES[25] == '06':
        print("预授权完成撤销[39]= %s"%isoAns.BITMAP_VALUES[39])
    else:
        print("The server dosen't understand my message!")

    return
