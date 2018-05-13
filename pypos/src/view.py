#!/usr/bin/python
#--*-- coding:utf-8 --*--

"""

(C) Copyright 2009 Igor V. Custodio

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

__author__ = "Steven Zheng (winchaozheng@gmail.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2012/05/07 9:50:00 $"
__copyright__ = "Copyright (c) 2012 Steven Zheng"
__license__ = "GPL"

def menu():
        print "*********************************"

        print "1. 签到          2. 消费"
        print "3. 撤销          4. 退货"
        print "5. 管理          6. 查询"
        print "7. 批量交易"
        print "0. 退出"

        print "*********************************"
        indata = raw_input("select a number:")
        if indata == "":
                num = -1
        else:
                num =int(indata)

        return num

def mngmenu():
        print "*********************************"

        print "1. 终端参数设置"
        print "2. 通讯参数设置"
        print "3. 终端密钥管理"
        print "4. 其他参数设置 "
        print "5. 显示所有参数"
	print "6. 列出所有交易"
	print "7. 删除所有流水"
        print "0. 返回上一级"

        print "*********************************"
        indata = raw_input("select a number:")
        if indata == "":
                num = -1
        else:
                num =int(indata)

        return num

def showconf(conf):
	print "================================="                                                  
        print "商户号：%s"%conf.get("main","mid")                                                  
        print "终端号：%s"%conf.get("main","tid")                                                  
        print "TPDU  : %s"%conf.get("main","tpdu")                                                 
        print "HEAD  : %s"%conf.get("main","head")                                                
        print "SEVRIP: %s"%conf.get("server","ip")                                                 
        print "PORT  : %s"%conf.get("server","port")                                               
        print "==================================" 

def showallssn(posdb,sqlite):
	conn = sqlite.connect(posdb)                                                       
        cur = conn.cursor()
        cur.execute("select * from posdata")
	res = cur.fetchall()
	for v in res:
		print v
	cur.close()
	conn.close()

def delallssn(posdb,sqlite):
	conn = sqlite.connect(posdb)                                                       
        cur = conn.cursor()
        cur.execute("delete from posdata")
	conn.commit()
	cur.close()
	conn.close()
	print "delete ok"
	
