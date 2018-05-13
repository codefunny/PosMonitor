#!/usr/bin/python

import sqlite3


dbname = 'posdb.db'
ctab = 'create table if not exists posdata(id integer primary key autoincrement,mti varchar(4),amt varchar(12),ssn varchar(6),batcode varchar(6),respcode varchar(2),msgtype varchar(5))'

idata = "insert into posdata(mti,amt,ssn,batcode,respcode,msgtype) values('0200','000000000001','000001','000012','00','IPER')"
sdata = 'select * from posdata'

conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute(ctab)
cur.execute(idata)
conn.commit()

cur.execute(sdata)
#res = cur.fetchall()
#print res

res1 = cur.fetchone()
print res1 
 

