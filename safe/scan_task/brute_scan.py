#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 下午4:13
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : brute_scan.py
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


def  brute_list(request):
    error=Log.objects.filter(log_level=3).order_by('-create_date')
    assets_list = Business_group.objects.filter(admin_user_id=request.user.id)
    data = Portpass_task.objects.filter(admin_user_id=request.user.id)
    dic_user=Dic.objects.filter(status=0)
    dic_pass=Dic.objects.filter(status=1)
    return render(request, 'task/brute_list.html', locals())

def  sub_brute_task(request,id):
    task_id=id
    return  render(request, 'task/brute_task.info.html', locals())
