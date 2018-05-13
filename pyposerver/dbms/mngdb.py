#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import time

"""
��ɾ�Ĳ�
����һ����¼��ɾ��һ����¼���޸�һ����¼����ѯһ����¼�����м�¼
"""

class oprdb:
    _conn = ''
    _cur = ''
    def __init__(self,sqlfd,dbname):
        self._conn = sqlfd.connect(dbname)
        self._cur = self._conn.cursor()
    def addOneItem(self,sqldata):
        try:
            self._cur.execute(sqldata)
        except sqlfd.Error as msg:
            print msg
            
    def delOneItem(self):pass
    def modOneItem(self):pass
    def selOneItem(self):pass
    def selAllItem(self):pass
    def closeDb(self):
        self._cur.close()
        self._conn.close()
        
dbname = 'dbms.db'

def exec_tbl(sqlfd,dbname,sqldata):
    conn = sqlfd.connect(dbname)
    cur = conn.cursor()
    try:
        cur.execute(sqldata)
    except sqlfd.Error as msg:
        print msg
        cur.close()
        conn.close()
    
    conn.commit()
    cur.close()
    conn.close()

    return
def selectAllData():pass
    
def drop_tbl(sqlfd,dbname,tblname):
    sqldata = "drop table %s"%tblname
    conn = sqlfd.connect(dbname)
    cur = conn.cursor()
    try:
        cur.execute(sqldata)
    except sqlfd.Error as msg:
        print msg
        cur.close()
        conn.close()

    conn.commit()
    cur.close()
    conn.close()

    return

def menu():
    print "1.����һ����¼    2.ɾ��һ����¼"
    print "3.�޸�һ����¼    4.��ѯһ����¼"
    print "5.��ʾ���м�¼"
    print "0.�˳�"
    inum = raw_input("��ѡ��->")

    return inum

def pan_opr():
    while 1:
        inum = menu()
        if inum.isdigit() == False:
            print "��������"
            continue
        
        inum = int(inum)
        if inum == 0:
            break
        elif inum ==1:
            icardid = raw_input("�����뿨�ţ�")
            icardname = raw_input("�����뿨���ƣ�")
            icardtype = raw_input("�����뿨���ͣ�")
            icardamt = raw_input("�����뿨��")
            iamtlimit = raw_input("�����뿨������ƣ�")
            icurrstatus = raw_input("�����뵱ǰ״̬��")
            iisscode = raw_input("�����뷢���д��룺")
            iissname = raw_input("�����뷢�������ƣ�")
            iupdatetime = time.strftime("%Y%m%d%H%M%S",time.localtime())

            sqldata = "insert into pan(card_id,card_name,card_type,card_amt,\
                        amt_limit,curr_status,iss_code,iss_name,update_time) values(\
                        '%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            sqldata %= (icardid,icardname,icardtype,icardamt,iamtlimit,icurrstatus,\
                        iisscode,iissname,iupdatetime)

            exec_tbl(sqlite3,dbname,sqldata)
            print "add one pan record"
        elif inum ==2:
            icardid = raw_input("������ɾ���Ŀ���:")
            sqldata = "delete from pan where card_id = '%s'"
            sqldata %=icardid

            exec_tbl(sqlite3,dbname,sqldata)
            print "delete one pan record"
        elif inum == 3:
            ocardid = raw_input("�������޸ĵĿ���:")
            sqldata = "select * from pan where card_id = '%s'"
            sqldata %=ocardid

            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            try:
                cur.execute(sqldata)
            except sqlfd.Error as msg:
                print msg
                cur.close()
                conn.close()
            v = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            if v == "" or v is None:
                print "there is no data"
                continue
            print v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]

            icardid = raw_input("�����뿨�ţ�")
            if icardid == "":icardid = v[1]
            icardname = raw_input("�����뿨���ƣ�")
            if icardname == "":icardname = v[2]
            icardtype = raw_input("�����뿨���ͣ�")
            if icardtype == "":icardtype = v[3]
            icardamt = raw_input("�����뿨��")
            if icardamt == "":icardamt = v[4]
            iamtlimit = raw_input("�����뿨������ƣ�")
            if iamtlimit == "":iamtlimit = v[5]
            icurrstatus = raw_input("�����뵱ǰ״̬��")
            if icurrstatus == "":icurrstatus = v[6]
            iisscode = raw_input("�����뷢���д��룺")
            if iisscode == "":iisscode = v[7]
            iissname = raw_input("�����뷢�������ƣ�")
            if iissname == "":iissname = v[8]
            iupdatetime = time.strftime("%Y%m%d%H%M%S",time.localtime())

            sqldata = "update pan set card_id='%s',card_name='%s',card_type='%s',\
                        card_amt='%s',amt_limit='%s',curr_status='%s',iss_code='%s',\
                        iss_name='%s',update_time='%s' where card_id='%s'"
            sqldata %= (icardid,icardname,icardtype,icardamt,iamtlimit,icurrstatus,\
                        iisscode,iissname,iupdatetime,ocardid)
            print sqldata

            exec_tbl(sqlite3,dbname,sqldata)
            print "modify one pan record"
        elif inum == 4:
            icardid = raw_input("�������ѯ�Ŀ���:")
            sqldata = "select * from pan where card_id = '%s'"
            sqldata %=icardid

            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            try:
                cur.execute(sqldata)
            except sqlfd.Error as msg:
                print msg
                cur.close()
                conn.close()
            v = cur.fetchone()
            #for v in result:
            print v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]
            conn.commit()
            cur.close()
            conn.close()
            print "select one pan record"
        elif inum == 5:
            sqldata = "select * from pan"
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            try:
                cur.execute(sqldata)
            except sqlfd.Error as msg:
                print msg
                cur.close()
                conn.close()
            result = cur.fetchall()
            for v in result:
                print v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]
            conn.commit()
            cur.close()
            conn.close()

        else:
            print "please again"


    return
    
def term_opr():pass
def merchant_opr():pass
def translog_opr():pass

while 1:
    print "1.������    2.�����ն˱�"
    print "3.�����̻���  4.������ʷ��"
    print "0.�˳�"
    inum = raw_input("��ѡ��->")
    if inum.isdigit() == False:
        print "��������"
        continue
    
    inum = int(inum)
    if inum == 0:
        break
    elif inum ==1:
        pan_opr()
    elif inum == 2:
        term_opr()
    elif inum == 3:
        merchant_opr()
    elif inum == 4:
        translog_opr()
    else:
        print "something happend!" 

print "done"

