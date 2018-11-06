#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/19 下午11:45
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : host_info.py
# @Software: PyCharm
from safe.models import *
import json
import  log
def  host_network(data,id,admin_user,ip):
    for k, v in json.loads(data).items():
        if k == "success":
            for x, y in v.items():
                t = y['stdout']
                w = t.split('\n')
                for i in w[2:]:
                    info = i.split()
                    if Assets_Host_Network.objects.filter( localaddress=info[3],foraddress=info[4],pid=info[6],assets_id=id):
                           Assets_Host_Network.objects.filter(localaddress=info[3],foraddress=info[4],pid=info[6],assets_id=id).update()
                    else:
                            Assets_Host_Network.objects.create(proto=info[0], recv=info[1], send=info[2], localaddress
                              =info[3],foraddress=info[4], status=info[5], pid=info[6], assets_id=id)
                            content = '发现了一个新的网络端口信息其内网为%s,外网为%s,进程的pid为%s' % (info[3], info[4], info[6])
                            log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=3)
    content = '更新了一个服务器网络端口信息'
    log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=0)

def  host_process(data,id,admin_user,ip):
    for k, v in json.loads(data).items():
        if k == "success":
            for x, y in v.items():
                t = y['stdout']
                w = t.split('\n')
                for i in w[1:]:
                    info = i.split()
                    if  Assets_Host_Process.objects.filter(user=info[0],command=info[10],assets_id=id):
                        Assets_Host_Process.objects.filter(user=info[0],command=info[10],assets_id=id).update()
                    else:
                         Assets_Host_Process.objects.create(user=info[0], pid=info[1], cpu=info[2], men
                         =info[3], vsz=info[4], rss=info[5], tty=info[6],stat=info[7],start=info[8],time=info[9],command=info[10], assets_id=id)
                         content = '发现了一个新的进程为%s,pid为%s,启动命令为%s' % (info[0], info[1], info[10])
                         log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=3)
    content = '更新了一个服务器资产进程信息'
    log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=0)



def  host_user(data,id,admin_user,ip):
    for k, v in json.loads(data).items():
        if k == "success":
            for x, y in v.items():
                t = y['stdout']
                w = t.split('\n')
                for info in w:
                    info=info.split(':')
                    print info
                    if Assets_Host_User.objects.filter(user=info[0],user_name=info[4],home=info[5],assets_id=id):
                        Assets_Host_User.objects.filter(user=info[0],user_name=info[4],home=info[5],assets_id=id).update()
                    else:
                        Assets_Host_User.objects.create(user=info[0], ps=info[1], uid=info[2], gid
                        =info[3], user_name=info[4], home=info[5], shell=info[6], assets_id=id)
                        content = '发现了一个新的用户为%s,宿主目录为%s' % (info[0], info[5])
                        log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=3)
    content = '更新了一个服务器资产用户信息'
    log.assets_info(ip=ip, user_id=admin_user, content=content, log_level=0)

