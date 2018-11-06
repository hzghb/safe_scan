#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 下午5:02
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : tasks.py.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
import celery
from celery import  shared_task
from IPy import IP
from  safe.Helper import nmapx
from safe.Helper import port_pass

from safe.Helper  import  brute_pass


# tasks.py

# @shared_task(bind=True)
# def port_scan(self,tgtHost):
#     print 1233
#     print  self.request
#     for i in IP(tgtHost):
#         ip=str(i)
#         nmapx.run(ip)
#     return  self.request


@shared_task(bind=True)
def scan_pass(self,assets_id,ip,tgtPort,user_id,task_id,):
    info=port_pass.Work(assets_id=assets_id,tgtHost=ip,tgtPort=tgtPort,user_id=user_id,task_id=task_id)
    info.run()
    return  'ok'


@shared_task(bind=True)
def brute_task(self,ip,username,userfile,passfile,scanmodel,threding,port,assets_id,task_id,user_id,):
     print scanmodel
     scan=brute_pass.scan(ip,username,userfile,passfile,scanmodel,threding,port,assets_id,task_id,user_id
                          )
     return  'ok'











