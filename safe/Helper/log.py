#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 下午4:45
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : log.py.py
# @Software: PyCharm
from safe.models import  *

def  login(ip,content,user_id,log_level):
     Log.objects.create(login_ip=ip,content=content,admin_user_id=user_id,log_type='用户登录' ,log_level=log_level)


def logout(ip, content, user_id,log_level):
     Log.objects.create(login_ip=ip, content=content, admin_user_id=user_id, log_type='用户退出', log_level=log_level)


def port_pass_log(ip, content, user_id,log_level):
     Log.objects.create(login_ip=ip, content=content, admin_user_id=user_id, log_type='端口弱口令扫描', log_level=log_level)

def assets_info (ip, content, user_id,log_level):
     Log.objects.create(login_ip=ip, content=content, admin_user_id=user_id, log_type='ansible主机信息获取', log_level=log_level)


def nsfocus_info(ip, content, user_id, log_level):
     Log.objects.create(login_ip=ip, content=content, admin_user_id=user_id, log_type='绿盟漏洞信息获取',
                        log_level=log_level)


def brute_info(ip, content, user_id, log_level):
     Log.objects.create(login_ip=ip, content=content, admin_user_id=user_id, log_type='弱口令扫描',
                        log_level=log_level)








