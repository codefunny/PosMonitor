#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3
import time

"""
增删改查
增加一条记录、删除一条记录、修改一条记录、查询一条记录和所有记录
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
    print "1.增加一条记录    2.删除一条记录"
    print "3.修改一条记录    4.查询一条记录"
    print "5.显示所有记录"
    print "0.退出"
    inum = raw_input("请选择->")

    return inum

def pan_opr():
    while 1:
        inum = menu()
        if inum.isdigit() == False:
            print "输入有误！"
            continue
        
        inum = int(inum)
        if inum == 0:
            break
        elif inum ==1:
            icardid = raw_input("请输入卡号：")
            icardname = raw_input("请输入卡名称：")
            icardtype = raw_input("请输入卡类型：")
            icardamt = raw_input("请输入卡余额：")
            iamtlimit = raw_input("请输入卡金额限制：")
            icurrstatus = raw_input("请输入当前状态：")
            iisscode = raw_input("请输入发卡行代码：")
            iissname = raw_input("请输入发卡行名称：")
            iupdatetime = time.strftime("%Y%m%d%H%M%S",time.localtime())

            sqldata = "insert into pan(card_id,card_name,card_type,card_amt,\
                        amt_limit,curr_status,iss_code,iss_name,update_time) values(\
                        '%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            sqldata %= (icardid,icardname,icardtype,icardamt,iamtlimit,icurrstatus,\
                        iisscode,iissname,iupdatetime)

            exec_tbl(sqlite3,dbname,sqldata)
            print "add one pan record"
        elif inum ==2:
            icardid = raw_input("请输入删除的卡号:")
            sqldata = "delete from pan where card_id = '%s'"
            sqldata %=icardid

            exec_tbl(sqlite3,dbname,sqldata)
            print "delete one pan record"
        elif inum == 3:
            ocardid = raw_input("请输入修改的卡号:")
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

            icardid = raw_input("请输入卡号：")
            if icardid == "":icardid = v[1]
            icardname = raw_input("请输入卡名称：")
            if icardname == "":icardname = v[2]
            icardtype = raw_input("请输入卡类型：")
            if icardtype == "":icardtype = v[3]
            icardamt = raw_input("请输入卡余额：")
            if icardamt == "":icardamt = v[4]
            iamtlimit = raw_input("请输入卡金额限制：")
            if iamtlimit == "":iamtlimit = v[5]
            icurrstatus = raw_input("请输入当前状态：")
            if icurrstatus == "":icurrstatus = v[6]
            iisscode = raw_input("请输入发卡行代码：")
            if iisscode == "":iisscode = v[7]
            iissname = raw_input("请输入发卡行名称：")
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
            icardid = raw_input("请输入查询的卡号:")
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
    print "1.管理卡表    2.管理终端表"
    print "3.管理商户表  4.管理历史表"
    print "0.退出"
    inum = raw_input("请选择->")
    if inum.isdigit() == False:
        print "输入有误！"
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

