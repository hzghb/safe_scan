#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 下午2:46
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : brute_pass.py.py
# @Software: PyCharm
import os
import uuid
import threading
from safe.Helper  import  SQL_db
def scan(ip,username,userfile,passfile,scanmodel,threding,port,assets_id,task_id,user_id):
    log = 'brute_log/' + str(uuid.uuid1())
    os.system('touch  %s' % log)
    if username == None:
        cmd = 'medusa -h %s -U %s -P %s -M %s  -t %s -O %s -n %s -F'% (
           ip, userfile, passfile, scanmodel,threding,log,port)
        print cmd
    else:
        cmd = 'medusa -h %s -u %s -P %s -M %s  -t %s -O %s -n %s -F' % (
            ip, username, passfile, scanmodel, threding,log,port)
    os.system(cmd)
    f= open(log, 'r')
    for line in f.readlines():
        if 'ACCOUNT FOUND' in line:
            ret= line.split(' ')
            SQL_db.pass_db(ip=ip,username=ret[6],password=ret[8],scanmodel=scanmodel,port=port,assets_id=assets_id,task_id=task_id,user_id=user_id)
            print '一切都结束了OK'
            return 'ok'
        elif  'Medusa has finished' in  line:
              print '任务结束写入数据库'
              return 'ok'
        else:
            continue




