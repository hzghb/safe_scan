#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 下午1:41
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : scan_task.py.py
# @Software: PyCharm
from rest_framework import serializers
from safe.models import  *
from rest_framework import viewsets,permissions
from safe.serializers import *
from safe.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from django.shortcuts import render,render_to_response,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from  safe.tasks  import *
from django.db.models import Q
from safe.Helper import Checkip

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_log(request,format=None):

    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Log.objects.filter(admin_user_id=request.user.id).count()
            draw = int(request.GET.get('draw'))
            start = int(request.GET.get('start'))  # 从多少行开始
            length = int(request.GET.get('length'))  # 显示多少条数据
            print draw
            print search
            print start
            print  length

            end = start + length  # 到多少行结束
            if search == "":
                print '3344'
                assets_values_list = Log.objects.filter(
                admin_user_id=request.user.id
                ).values_list(
                    'id',
                    'create_date',
                    'admin_user_id',
                    'login_ip',
                    'log_level',
                    'log_type',
                    'content',
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                search_list = Log.objects.filter(
                    admin_user_id=request.user.id and
                    Q(login_ip__contains=search) |
                    Q(log_type__contains=search) |
                    Q(content__contains=search)
                ).values_list(
                    'id',
                    'create_date',
                    'admin_user_id',
                    'login_ip',
                    'log_level',
                    'log_type',
                    'content',
                ).order_by('-id')[start: end]

                _filter = len(Log.objects.filter(
                    admin_user_id=request.user.id and
                    Q(login_ip__contains=search)|
                    Q(log_type__contains=search)|
                    Q(content__contains=search)
                ).values_list(
                    'id',
                    'create_date',
                    'admin_user_id',
                    'login_ip',
                    'log_level',
                    'log_type',
                    'content',
                ).order_by('-id'))
                all_lists = map(list, search_list)
                print all_lists

            all_list = []
            for i in all_lists:
                i[1] = (i[1]).strftime('%Y-%m-%d %H:%M:%S')
                i[2] = User.objects.filter(id=i[2]).values_list('username', flat=True)[0]
                i[4] = Log.objects.get(log_level=i[4], id=i[0]).get_log_level_display()
                all_list.append(i)
            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered':_filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))