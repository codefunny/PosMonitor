#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3

dbname = 'dbms.db'
"""
id,卡号，卡名称，卡类型（00未指明，01借记卡，02贷记卡），卡金额，金额限制，
当前状态（00可用状态，01失效卡，02挂失卡，03被窃卡，04过期卡），
发卡行代码，发卡行名称，更新时间
"""
pan_tbl = "create table if not exists pan(\
            id integer primary key autoincrement,\
            card_id varchar(19) unique,\
            card_name varchar(30),\
            card_type varchar(2),\
            card_amt varchar(12),\
            amt_limit varchar(12),\
            curr_status varchar(2),\
            iss_code varchar(8),\
            iss_name varchar(30),\
            update_time varchar(14)\
            )"

"""
id,终端号，商户号，当前状态，签到标识（0签到，1未签到）
主密钥，pinkey，mackey，是否校验mac（0校验，1不校验）
批次号，清算日期，更新时间
"""
term_tbl = "create table if not exists term(\
            id integer primary key autoincrement,\
            code varchar(12) unique,\
            mer_code varchar(15),\
            status varchar(2),\
            logon varchar(1),\
            master_key char(32),\
            pin_key char(32),\
            mac_key char(32),\
            mac_enacle char(1),\
            bat_code char(6),\
            sett_date char(4),\
            update_time char(14)\
            )"

"""
id,商户号，商户名称，商户结算行标识，
商户类型，当前状态（0使用状态，1未启用状态），更新时间
"""
merchant_tbl = "create table if not exists merchant(\
            id integer primary key autoincrement,\
            code varchar(15) unique,\
            name varchar(30),\
            merc_bank varchar(11),\
            merc_type varchar(4),\
            status varchar(1),\
            update_time char(14)\
            )"

"""
iss_code 发卡行代码
acq_code 收单行代码通merc_bank
"""
translog_tbl = "create table if not exists translog(\
            log_key varchar(20),\
            sett_date varchar(4),\
            bat_code varchar(6),\
            iss_code varchar(11),\
            msg_type varchar(4),\
            pan varchar(19),\
            proc_code varchar(6),\
            txn_amt varchar(12),\
            txn_ssn varchar(6),\
            txn_time varchar(6),\
            txn_date varchar(4),\
            entry_mode varchar(2),\
            acq_code varchar(11),\
            rrn varchar(12),\
            auth_code varchar(6),\
            resp_code varchar(2),\
            comp_flag varchar(2),\
            tid varchar(12),\
            mid varchar(15),\
            tran_curr varchar(3),\
            addi_data varchar(100),\
            update_time varchar(14),\
            primary key (log_key)\
            )"
            

idata = "insert into posdata(mti,amt,ssn,batcode,respcode,msgtype) values('0200','000000000001','000001','000012','00','IPER')"
sdata = 'select * from posdata'

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

"""
建表
"""
while 1:
    print "1. 建卡表       2. 删卡表"
    print "3. 建终端表     4. 删终端表"
    print "5. 建商户表     6. 删商户表"
    print "7. 建历史表     8. 删历史表"
    print "9. 建以上表     10.删以上表"
    print "0. 退出"
    inum = raw_input("请选择->")
    inum = int(inum)

    if inum == 0:
        break
    elif inum == 1:
        exec_tbl(sqlite3,dbname,pan_tbl)
    elif inum == 3:
        exec_tbl(sqlite3,dbname,term_tbl)
    elif inum == 5:
        exec_tbl(sqlite3,dbname,merchant_tbl)
    elif inum == 7:
        exec_tbl(sqlite3,dbname,translog_tbl)
    elif inum == 9:
        exec_tbl(sqlite3,dbname,pan_tbl)
        exec_tbl(sqlite3,dbname,term_tbl)
        exec_tbl(sqlite3,dbname,merchant_tbl)
        exec_tbl(sqlite3,dbname,translog_tbl)
        
    elif inum == 2:
        drop_tbl(sqlite3,dbname,"pan")
    elif inum == 4:
        drop_tbl(sqlite3,dbname,"term")
    elif inum == 6:
        drop_tbl(sqlite3,dbname,"merchant")
    elif inum == 8:
        drop_tbl(sqlite3,dbname,"translog")
    elif inum == 10:
        drop_tbl(sqlite3,dbname,"pan")
        drop_tbl(sqlite3,dbname,"term")
        drop_tbl(sqlite3,dbname,"merchant")
        drop_tbl(sqlite3,dbname,"translog")
    else:
        print "error input"

    print "done"

