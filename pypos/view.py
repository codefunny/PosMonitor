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

        print("1. ǩ��            2. ����")
        print("3. ����            4. �˻�")
        print("5. ����            6. ��ѯ")
        print("7. ���ѳ���         8.��������")
        print("9. Ԥ��Ȩ ")
        print("10.Ԥ��Ȩ����")
        print("11.Ԥ��Ȩ�������")
        print("12.Ԥ��Ȩ��ɳ���")
        print("13. ��������")
        print("0. �˳�")

        print("*********************************")
        indata = raw_input("select a number:")
        if indata == "" or indata.isdigit() == False:
                num = -1
        else:
                num =int(indata)

        return num

def mngmenu():
        print("*********************************")

        print("1. �ն˲�������")
        print("2. ͨѶ��������")
        print("3. �ն���Կ����")
        print("4. ������������ ")
        print("5. ��ʾ���в���")
        print("6. �г����н���")
        print("7. ɾ��������ˮ")
        print("0. ������һ��")

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
        print("�̻��� ��%s"%itemsMain["mid"])
        print("�ն˺� ��%s"%itemsMain["tid"])                                                
        print("TPDU  : %s"%itemsMain["tpdu"])                                                 
        print("HEAD  : %s"%itemsMain["head"])                                               
        print("SEVRIP: %s"%itemsServer["ip"])                                               
        print("PORT  : %s"%itemsServer["port"])                                              
        print("==================================" )


	
