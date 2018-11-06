#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 下午5:22
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : port_api.py.py
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

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_port_task(request,format=None):

    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Portpass_task.objects.filter(admin_user_id=request.user.id).count()
            draw = int(request.GET.get('draw'))
            start = int(request.GET.get('start'))  # 从多少行开始
            length = int(request.GET.get('length'))  # 显示多少条数据
            end = start + length  # 到多少行结束
            if search == "":
                assets_values_list = Portpass_task.objects.filter(
                admin_user_id=request.user.id
                ).values_list(
                    'portpass_tgthost',
                    'portpass_name',
                    'portpass_status',
                    'admin_user_id',
                    'id',
                    'start_date',
                    'end_date'
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                search_list = Portpass_task.objects.filter(
                    Q(portpass_tgthost=search)|
                    Q(portpass_name=search)


                ).values_list(
                    'portpass_tgthost',
                    'portpass_name',
                    'portpass_status',
                    'admin_user_id',
                    'id',
                    'start_date',
                    'end_date'
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)
            all_list = []
            for i in all_lists:
                i[2] = Portpass_task.objects.get(portpass_status=i[2], id=i[4]).get_portpass_status_display()
                i[3] = User.objects.filter(id=i[3]).values_list('username',flat=True)[0]
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))


@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def  add_port_task(request,format=None):
 if request.method == 'POST':
        if(request.data.get('data')):
            data =  request.data.get('data')
            data['admin_user_id']=request.user.id
            data['portpass_tgthost'] =str(data["portpass_tgthost"])
            print request.user.id
        else:
            data = request.data
        #print  data
        serializer = Portpass_task_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def del_port_task(request,format=None):
    if request.method == 'DELETE':
        if (request.data.get('data')):
            data = request.data.get('data')
            print data
            for data_id in data:
                print  data_id
                Portpass_task.objects.filter(id=int(data_id)).delete()
            return HttpResponse('200', status=200)
        else:
            return HttpResponse('200', status=200)





@api_view([ 'GET', 'POST',])
@csrf_exempt
def port_start_task(request, id, format=None):
    if request.method == 'GET':
        task_info = Portpass_task.objects.get(id=id)
        assets_id_list = json.loads(task_info.portpass_tgthost)
        print assets_id_list
        for assets_id in assets_id_list:
            if Assets.objects.filter(id=assets_id).exists():
                print '****************************************'
                ip = (Assets.objects.get(id=assets_id)).assets_ip
                tgtPort=(task_info.portpass_port).decode('utf-8')
                task=scan_pass.delay(
                                assets_id=assets_id,
                                ip=ip,
                                tgtPort=tgtPort,
                                user_id=request.user.id,
                                task_id=id,
                                )
                Sub_task.objects.create(sub_task_id=task.id,task_scan_id=id,ip=ip)
        else:
            pass
        return HttpResponse('200', status=200)



@api_view([ 'GET', 'POST',])
@csrf_exempt
def get_sub_port_task(request, id, format=None):
    if request.method == 'GET':
        search = request.GET.get('search[value]')
        asset_count = Sub_task.objects.filter(task_scan_id=id).count()
        draw = int(request.GET.get('draw'))
        start = int(request.GET.get('start'))  # 从多少行开始
        length = int(request.GET.get('length'))  # 显示多少条数据
        end = start + length  # 到多少行结束
        if search == "":
            assets_values_list =Sub_task.objects.filter(
             task_scan=id
            ).values_list(
                'id',
                'ip',
                'sub_task_id',
                'start_date',
                'end_date',
                'kwargs',
                'worker',
                'Result'
            ).order_by('-id')[start: end]
            _filter = asset_count
            all_lists = map(list, assets_values_list)
        all_list = []
        for i in all_lists:
            try:
             i[3]=(i[3]).strftime('%Y-%m-%d %H:%M:%S')
            except:
                i[3] = 'None'
            try:
              i[4] = (i[4]).strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
            print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
            print i[2]
            result=TaskState.objects.get(task_id=i[2])
            i[5]=str(result.kwargs)
            print i[5]
            i[6]=str(result.worker)
            i[7]=str(result.result)
            i[2] = (AsyncResult(i[2])).status
            all_list.append(i)
        data = {
            'draw': draw,
            'recordsTotal': asset_count,
            'recordsFiltered': _filter,
            'data': all_list
        }
        return HttpResponse(json.dumps(data))

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_sub_port_info(request,id,format=None):

    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Scan_port.objects.filter(admin_user_id=request.user.id,task_scan_id=id).count()
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
                assets_values_list =Scan_port.objects.filter(
                    Q(admin_user_id=request.user.id) ,
                    Q(task_scan_id=id)



                ).values_list(
                    'id',
                    'ip',
                    'port_number',
                    'protocal',
                    'banner',
                    'create_date',
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                print search
                search_list = Scan_port.objects.filter(
                    Q(admin_user_id=request.user.id),
                    Q(task_scan_id=id)

                ).values_list(
                    'id',
                    'ip',
                    'port_number',
                    'protocal',
                    'banner',
                    'create_date',
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)
                print all_lists

            all_list = []
            for i in all_lists:
                i[5]=(i[5]).strftime('%Y-%m-%d %H:%M:%S')
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))



