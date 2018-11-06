#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 下午4:10
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : pass_port.py.py
# @Software: PyCharm

#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from safe.Helper import Checkcode
import StringIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from safe.models import    *
from safe.Helper  import   log
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json


def  task_list(request):
    error=Log.objects.filter(log_level=3).order_by('-create_date')
    assets_list = Business_group.objects.filter(admin_user_id=request.user.id)
    data = Portpass_task.objects.filter(admin_user_id=request.user.id)
    dic_user=Dic.objects.filter(status=0)
    dic_pass=Dic.objects.filter(status=1)
    return render(request, 'task/task_list.html', locals())

def  sub_port_task(request,id):
    task_id=id
    return  render(request, 'task/task.info.html', locals())
