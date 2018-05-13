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

    newBat = raw_input("�������µ����κţ�")
    if newBat == "" or newBat.isspace():
        newBat = oldBat
    elif len(newBat) > 6 or newBat.isdigit() != True:
        print "��������κű���Ϊ����"
        return
    
    newSsn = raw_input("�������µ���ˮ�ţ�")
    if newSsn == "" or newSsn.isspace():
        newSsn = oldSsn
    elif len(newSsn) > 6 or newSsn.isdigit() != True:
        print "�������ˮ�ű���Ϊ����"
        return
    
    newTime = raw_input("�������µĳ�ʱʱ�䣺")
    if newTime == "" or newTime.isspace():
        newTime = oldTime
    elif newTime.isdigit() != True:
        print "����ĳ�ʱʱ�����Ϊ����"
        return
    
    newEcho = raw_input("�������µ���������")
    if newEcho == "" or newEcho.isspace():
        newEcho = oldEcho
    elif newEcho.isdigit() != True:
        print "��������ڱ���Ϊ����"
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
    print("now BatCode��%s"%newBat)
    print("now LocalSsn��%s"%newSsn)
    print("now SleepTime��%s"%newTime)
    print("now NumEcho��%s"%newEcho)
    
    return

def chMkeyPara(conf):
    oldMk = conf.getValue("mkey","mk")
    print "TMK : %s\n"%oldMk
    
    newMk = raw_input("�������µ�TMK��")
    if newMk == "" or newMk.isspace():
        newMk = oldMk
    elif len(newMk)!=32 or newMk.isalnum() != True:
        print "�������Կ�ɷ���Ϊ���ֺ���ĸ"
        return
    
    conf.setValue("mkey","mk",newMk)
    print("now TMK��%s"%newMk)

    return

def chLinePara(conf,outdata):
    #pypos = re.compile(r"(((2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(((2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.)")
    items = conf.getItems("server")
    oldIp = items["ip"]
    oldPort = items["port"]
    print "IP : %s,PORT : %s\n"%(oldIp,oldPort)
    
    newIp = raw_input("�������µ�IP��")
    if newIp == "" or newIp.isspace():
        newIp = oldIp
    
    newPort = raw_input("�������µ�PORT��")
    if newPort == "" or newPort.isspace():
        newPort = oldPort

    outdata.append(newIp)
    outdata.append(newPort)
    newItems = [["server","ip",newIp],\
                ["server","port",newPort]]
    conf.setMulValue(newItems)
    print("now IP��%s"%newIp)
    print "now Port:%s"%newPort

    return

def chTermPara(conf,outdata):
    #global mid,tid
    items = conf.getItems("main")
    oldmid = items["mid"]
    oldtid = items["tid"]
    oldtpdu = items["tpdu"]
    oldhead = items["head"]
    print("ԭ�̻��ţ�%s"%oldmid)
    print("ԭ�ն˺ţ�%s"%oldtid)
    print("ԭTPDU��%s"%oldtpdu)
    print("ԭ����ͷ��%s"%oldhead)
    
    newmid = raw_input("���������̻��ţ�")
    if newmid =="" or newmid.isspace():
            newmid = oldmid
    if len(newmid)!=15 or newmid.isalnum()!=True:
            print("�̻��ű���Ϊ15λ,��Ϊ������ĸ!")
            return

    newtid = raw_input("���������ն˺ţ�")
    if newtid =="" or newtid.isspace():
            newtid = oldtid
    if len(newtid)!=8 or newtid.isdigit()!=True:
            print("�ն˺ű���Ϊ8λ����Ϊ���֣�")
            return
        
    newtpdu = raw_input("��������TPDU��")
    if newtpdu =="" or newtpdu.isspace():
            newtpdu = oldtpdu
    if len(newtpdu)!=10 or newtpdu.isdigit()!=True:
            print("TPDU����Ϊ10λ����Ϊ���֣�")
            return
        
    newhead = raw_input("�������±���ͷ��")
    if newhead =="" or newhead.isspace():
            newhead = oldhead
    if len(newhead)!=12 or newhead.isdigit()!=True:
            print("����ͷ����Ϊ12λ����Ϊ���֣�")
            return
        
    outdata.append(newmid)
    outdata.append(newtid)
    outdata.append(newtpdu)
    outdata.append(newhead)
    newItems = [["main","mid",newmid],["main","tid",newtid],
                ["main","tpdu",newtpdu],["main","head",newhead]]
    conf.setMulValue(newItems)
    print("���̻��ţ�%s"%outdata[0])
    print("���ն˺ţ�%s"%outdata[1])
    print("��TPDU��%s"%outdata[2])
    print("�±���ͷ��%s"%outdata[3])

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

"""����һ����¼"""
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

"""�������һ�ʽ���"""
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

"""����һ�����ݵ����ݿ�"""
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

"""��ȡsocket��fd"""
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

"""����inItems���д��"""
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

"""����˻��������������"""
def checkRetData():
    ret = True
    errnum = 0
    bkamtstr = ""
    bkrrnstr = ""
    bkdatestr = ""
    
    while errnum < 3 :
        errnum += 1
        bkamt = raw_input("�������(��1200��ʾ12Ԫ)")
        if bkamt == "" or bkamt.find('.') == True or len(bkamt)>12:
            print("����������")
        else:
            bkamtstr = bkamt.zfill(12)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkrrn = raw_input("������ԭ�ο��ţ�")
        if bkrrn == "" or bkrrn.isdigit() == False or len(bkrrn)>12:
            print("����ο�������")
        else:
            bkrrnstr = bkrrn.zfill(12)
            break
        if errnum == 3:
            ret = False
            break

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkdate = raw_input("���������ڣ�")
        if bkdate == "" or bkdate.isdigit() == False or len(bkdate)>4:
            print("������������")
        else:
            bkdatestr = bkdate.zfill(4)
            break
        if errnum == 3:
            ret = False
            return ret
        
    return (bkamtstr,bkrrnstr,bkdatestr)

"""������ѽ��׵��������"""
def checkTpayData():
    ret = True
    amtstr = ""
    errnum = 0
    while errnum < 3 :
        errnum += 1
        amt = raw_input("�������(��1200��ʾ12Ԫ)")
        if amt == "" or amt.find('.') == True or len(amt)>12:
            print("����������")
        else:
            amtstr = amt.zfill(12)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        passwd = raw_input("���������룺")
        if passwd != "" and len(passwd) != 6:
            print("���볤�ȹ̶�Ϊ6λ��")
        else:
            break

        if errnum == 3:
            ret = False
            return ret
 
    return amtstr,passwd

"""������ѳ������������"""
def checkTrevData():
    ret = True
    ossnstr = ""
    errnum = 0
    while errnum < 3 :
        errnum += 1
        ossn = raw_input("������ԭƾ֤�ţ�")
        if ossn == "" or ossn.isdigit() == False or len(ossn)>6:
            print("����ƾ֤������")
        else:
            ossnstr = ossn.zfill(6)
            break
        if errnum == 3:
            ret = False
            return ret
    return ossnstr

"""���Ԥ��Ȩ�����"""
def checkPadData():
    ret = True
    errnum = 0
    bkamtstr = ""
    bkrrnstr = ""
    bkdatestr = ""

    errnum = 0
    while errnum < 3 :
        errnum += 1
        bkdate = raw_input("���������ڣ�")
        if bkdate == "" or bkdate.isdigit() == False or len(bkdate)>4:
            print("������������")
        else:
            bkdatestr = bkdate.zfill(4)
            break
        if errnum == 3:
            ret = False
            return ret

    errnum = 0
    while errnum < 3 :
        errnum += 1
        authcode = raw_input("��������Ȩ�ţ�")
        if authcode == "" or authcode.isdigit() == False or len(authcode)>6:
            print("������Ȩ������")
        else:
            authcode = authcode.zfill(6)
            break
        if errnum == 3:
            ret = False
            break
        
    while errnum < 3 :
        errnum += 1
        bkamt = raw_input("�������(��1200��ʾ12Ԫ)")
        if bkamt == "" or bkamt.find('.') == True or len(bkamt)>12:
            print("����������")
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
        print("������Ӧ[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':         
            outdata = ['0200',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),isoAns.BITMAP_VALUES[37].zfill(12),\
                         lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],isoAns.BITMAP_VALUES[39],TRANTYPE[0],isoAns.BITMAP_VALUES[12],\
                       isoAns.BITMAP_VALUES[13]]     
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "�������ݿ�ʧ��,xiaofei"
        else:
            print("xiaofei")
    elif mtistr == '0410' and v1[1]['value'] == '000000' and isoAns.BITMAP_VALUES[25] == '00':
        print("���ѳ���[39]= %s"%isoAns.BITMAP_VALUES[39])
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
        print("���ѳ���[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':
            outdata = ['0200',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),\
                       isoAns.BITMAP_VALUES[37].zfill(12),lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],\
                       isoAns.BITMAP_VALUES[39],TRANTYPE[1],isoAns.BITMAP_VALUES[12],isoAns.BITMAP_VALUES[13]]
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "�������ݿ�ʧ��"
        else:
            print("xiaofeichexiao")
    elif mtistr == '0230' and v1[1]['value'] == '200000' and isoAns.BITMAP_VALUES[25] == '00':
        print("�˻�[39]= %s"%isoAns.BITMAP_VALUES[39])
    elif mtistr == '0110' and v1[1]['value'] == '030000' and isoAns.BITMAP_VALUES[25] == '06':
        print("Ԥ��Ȩ[39]= %s"%isoAns.BITMAP_VALUES[39])
            
    elif mtistr == '0210' and v1[1]['value'] == '000000' and isoAns.BITMAP_VALUES[25] == '06':
        print("Ԥ��Ȩ���[39]= %s"%isoAns.BITMAP_VALUES[39])
        if isoAns.BITMAP_VALUES[39] == '00':
            outdata = ['0100',iso.ASCII_VALUES[4].zfill(12),isoAns.BITMAP_VALUES[11].zfill(6),\
                       isoAns.BITMAP_VALUES[37].zfill(12),lbatcode.zfill(6),isoAns.BITMAP_VALUES[38],\
                       isoAns.BITMAP_VALUES[39],TRANTYPE[5],isoAns.BITMAP_VALUES[12],isoAns.BITMAP_VALUES[13]]
            ret = insertOneData(posdb,sqlite3,outdata)
            if ret == False:
                print "�������ݿ�ʧ��"
        else:
            print("yushouquan")
    elif mtistr == '0210' and v1[1]['value'] == '200000' and isoAns.BITMAP_VALUES[25] == '06':
        print("Ԥ��Ȩ��ɳ���[39]= %s"%isoAns.BITMAP_VALUES[39])
    else:
        print("The server dosen't understand my message!")

    return
