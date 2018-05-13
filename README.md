# PosMonitor
monitor of pos and pos server

#前言

几年前，因为开发和测试的需要，我尝试写一个POS模拟器，当时对Python和Perl作了个调研，最后采用了Python，并有一个ISO8583的第三方库可供使用，于是经过几个迭代，在当年的5月份完成一个稳定版，后来几年的使用版本都是在这个版本基础上的变体，今天看来当时的源码还有诸多可改进的地方，所以把这个版本开源了，给有需要或有兴趣的同学去完成吧。

#版本说明：
使用Python2.7

客户端模拟器
cd pypos
python pypos.py

服务端模拟器
cd pyposserver
python pyposserver
