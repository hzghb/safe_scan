#!coding:utf-8
import optparse, re, subprocess, socket, time, os, nmap,time ,uuid,sys
from threading import *
from IPy import IP
from  safe.Helper import SQL_db
from safe.models import  *
import django.utils.timezone as timezone

def  scan_port(assets_id,tgtHost,port,user_id,task_id,):
    print tgtHost
    r = os.popen('nmap  %s  -p %s' %(tgtHost,port))
    info = []
    for port in r.readlines():
        if '/tcp' in port.strip():
            port_list = port.strip().split(' ')
            while '' in port_list: port_list.remove('')
            info.append(port_list)
    SQL_db.port_db(assets_id=assets_id,ip=tgtHost,info=info,task_id=task_id, user_id=user_id)
    print info
    return info

