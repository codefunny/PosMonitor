#!/usr/bin/python
# -*- coding: cp936 -*-

import sqlite3

dbname = 'dbms.db'
"""
id,���ţ������ƣ������ͣ�00δָ����01��ǿ���02���ǿ���������������ƣ�
��ǰ״̬��00����״̬��01ʧЧ����02��ʧ����03���Կ���04���ڿ�����
�����д��룬���������ƣ�����ʱ��
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
id,�ն˺ţ��̻��ţ���ǰ״̬��ǩ����ʶ��0ǩ����1δǩ����
����Կ��pinkey��mackey���Ƿ�У��mac��0У�飬1��У�飩
���κţ��������ڣ�����ʱ��
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
id,�̻��ţ��̻����ƣ��̻������б�ʶ��
�̻����ͣ���ǰ״̬��0ʹ��״̬��1δ����״̬��������ʱ��
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
iss_code �����д���
acq_code �յ��д���ͨmerc_bank
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
����
"""
while 1:
    print "1. ������       2. ɾ����"
    print "3. ���ն˱�     4. ɾ�ն˱�"
    print "5. ���̻���     6. ɾ�̻���"
    print "7. ����ʷ��     8. ɾ��ʷ��"
    print "9. �����ϱ�     10.ɾ���ϱ�"
    print "0. �˳�"
    inum = raw_input("��ѡ��->")
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

