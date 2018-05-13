# -*- coding: cp936 -*-
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
        print("*********************************")

        print("1. 签到            2. 消费")
        print("3. 撤销            4. 退货")
        print("5. 管理            6. 查询")
        print("7. 消费冲正         8.撤销冲正")
        print("9. 预授权 ")
        print("10.预授权撤销")
        print("11.预授权完成请求")
        print("12.预授权完成撤销")
        print("13. 批量交易")
        print("0. 退出")

        print("*********************************")
        indata = raw_input("select a number:")
        if indata == "" or indata.isdigit() == False:
                num = -1
        else:
                num =int(indata)

        return num

def mngmenu():
        print("*********************************")

        print("1. 终端参数设置")
        print("2. 通讯参数设置")
        print("3. 终端密钥管理")
        print("4. 其他参数设置 ")
        print("5. 显示所有参数")
        print("6. 列出所有交易")
        print("7. 删除所有流水")
        print("0. 返回上一级")

        print("*********************************")
        indata = raw_input("select a number:")
        if indata == "":
                num = -1
        else:
                num =int(indata)

        return num

def showconf(conf):
        itemsMain = conf.getItems("main")
        itemsServer = conf.getItems("server")
        print("=================================")                                              
        print("商户号 ：%s"%itemsMain["mid"])
        print("终端号 ：%s"%itemsMain["tid"])                                                
        print("TPDU  : %s"%itemsMain["tpdu"])                                                 
        print("HEAD  : %s"%itemsMain["head"])                                               
        print("SEVRIP: %s"%itemsServer["ip"])                                               
        print("PORT  : %s"%itemsServer["port"])                                              
        print("==================================" )


	
