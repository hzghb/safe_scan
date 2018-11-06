#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 下午5:02
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : nmapx.py
# @Software: PyCharm


import optparse, re, subprocess, socket, time, os, nmap, MySQLdb
from threading import *
from IPy import IP
import commands

connection_lock_1 = BoundedSemaphore(value=1000)
connection_lock_2 = BoundedSemaphore(value=5)


def nmapscan(ip, port):
    print port
    nm = nmap.PortScanner()
    ret = nm.scan(ip, port)
    timestramp = str(ret['nmap']['scanstats']['timestr']).strip()
    portstate = str(ret['scan'][ip]['tcp'][int(port)]['state']).strip()
    servicename = str(ret['scan'][ip]['tcp'][int(port)]['name']).strip()
    serviceversion = str(
        str(ret['scan'][ip]['tcp'][int(port)]['product']) + str(ret['scan'][ip]['tcp'][int(port)]['version'])).strip()
    print port, servicename, serviceversion


def pass_scan(ip,user,password,scanmodel,port):
     print user
     print ip
     cmd='medusa -h %s -u %s -P %s -M %s -n %d -t 100' %(ip,user,password,scanmodel,port)
     (status, output) = commands.getstatusoutput(cmd)
     rx='ACCOUNT FOUND(.*)[SUCCESS]'
     if re.findall(rx,output):
           print 'ok'
     else:
        print 'bad'
     return  122

def connPort(ip, port):
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    st.settimeout(1)
    try:
        st.connect((ip, int(port)))
        nmapscan(ip, port)
        st.close()
    except Exception as e:
        pass
    connection_lock_1.release()


def portScan(ip, port_list):
        for port in port_list:
            connection_lock_1.acquire()
            t = Thread(target=connPort, args=(ip, port))
            t.start()


def arr_port(tgtPort):
    port_list2 = tgtPort.split('-')
    start_num = int(port_list2[0]) + 1
    end_num = int(port_list2[1])
    for j in range(start_num, end_num):
        port_list2.append(str(j))
    return port_list2


def run(tgtHost):
    time.localtime()
    port_list = arr_port('1-65535')
    portScan(tgtHost, port_list)

