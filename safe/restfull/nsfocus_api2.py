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
from djcelery.models import  *
from celery.result import AsyncResult
from safe.Helper import  nsfocus
from safe.Helper import  SQL_db

@api_view([ 'DELETE','GET', 'POST',])
@csrf_exempt
def get_nsfocus_task(request, format=None):
    if request.method == 'GET':
        search = request.GET.get('search[value]')
        asset_count =Nsfocus_task.objects.all().count()
        draw = int(request.GET.get('draw'))
        start = int(request.GET.get('start'))  # 从多少行开始
        length = int(request.GET.get('length'))  # 显示多少条数据
        end = start + length  # 到多少行结束
        if search == "":
            all_assets_obj= Nsfocus_task.objects.filter().order_by('-id')[start:end]
            _filter = asset_count

        else:
            filter_list = Nsfocus_task.objects.filter(
                              Q(nsfocus_tgthost=search) |
                              Q(nsfocus_name=search) ).order_by('-id')
            all_assets_obj=filter_list[start:end]

            _filter = len(filter_list)

        all_list = []
        for assets in  all_assets_obj:
            info=[]
            info.append(assets.id)
            info.append(assets.nsfocus_tgthost)
            info.append(assets.nsfocus_name)
            info.append(assets.nsfocus_desc)
            info.append(assets.admin_user.username)
            print '**************************'
            print assets.nsfocus_task_id
            if assets.nsfocus_task_id !=None:
                result=task_status(assets)
                info.append(result['status'])
                info.append(result['time_start_scan'])
                info.append(result['time_end_scan'])
            else:
                info.append(assets.get_nsfocus_status_display())
                info.append(assets.start_date)
                info.append(assets.end_date)
            info.append(assets.nsfocus_task_id)
            all_list.append(info)
        data = {
            'draw': draw,
            'recordsTotal': asset_count,
            'recordsFiltered': _filter,
            'data': all_list
        }

        return HttpResponse(json.dumps(data))


@api_view(['DELETE', 'GET', 'POST', ])
@csrf_exempt
def add_nsfocus_task(request, format=None):
    if request.method == 'POST':
        if (request.data.get('data')):
            data = request.data.get('data')
            data['admin_user_id'] = request.user.id
            data['nsfocus_tgthost'] = str(data["nsfocus_tgthost"])
            data['nsfocus_port_level'] = int(data['nsfocus_port_level'])
            data['nsfocus_level'] = int(data['nsfocus_level'])
            print request.user.id
        else:
            data = request.data
        # print  data
        serializer = Nsfocus_task_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'GET', 'POST', ])
@csrf_exempt
def del_nsfocus_task(request, format=None):
    if request.method == 'DELETE':
        if (request.data.get('data')):
            data = request.data.get('data')
            print data
            for data_id in data:
                print  data_id
                Nsfocus_task.objects.filter(id=int(data_id)).delete()
            return HttpResponse('200', status=200)
        else:
            return HttpResponse('200', status=200)



def  task_status(assets):
     id=assets.id
     print '*************************************************************'
     dev_id=assets.nsfocus_dev
     print dev_id
     print type(dev_id)
     nsfocus_id=str(assets.nsfocus_task_id)
     info=nsfocus.Work(0)
     ret=info.task__status(nsfocus_id)
     return  ret






@api_view([ 'GET', 'POST',])
@csrf_exempt
def start_nsfocus_task(request, id, format=None):
    if request.method == 'GET':
        task_arg=Nsfocus_task.objects.get(id=id)
        print task_arg.nsfocus_tgthost
        ret=nsfocus.Work(dev_id=task_arg.nsfocus_dev)
        ret.create_xml(targets=task_arg.nsfocus_tgthost,taskname=task_arg.nsfocus_name,
                       live=task_arg.nsfocus_active, port_strategy_userports=task_arg.nsfocus_port,
                       port_speed=str(task_arg.nsfocus_port_level), scan_level=str(task_arg.nsfocus_level)

                       )
        result=ret.addtask()
        result = json.loads(result)
        print result['ret_msg']
        if  result['ret_msg']=='success':
            task_id=result['data']['task_id']
            Nsfocus_task.objects.filter(id=id).update(nsfocus_status=2,nsfocus_task_id=int(task_id))
            return HttpResponse('200', status=200)
        else:
            return HttpResponse('200', status=200)
    else:
        return HttpResponse('200', status=200)






def get_nsfocus_report(request, id, format=None):
    if request.method == 'GET':
             arg=Nsfocus_task.objects.get(id=id)
             admin_user_id=request.user.id
             ret = nsfocus.Work(dev_id=arg.nsfocus_dev)
             print arg.id
             print arg.nsfocus_dev
             nsfocus_task_id= str(arg.nsfocus_task_id)
             result=ret.task__result(nsfocus_task_id)
             SQL_db.vul_db(id=id,nsfocus_task_id=nsfocus_task_id,result=result,admin_user_id=admin_user_id)
             return HttpResponse('200', status=200)
