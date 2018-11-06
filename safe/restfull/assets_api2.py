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
from safe.Helper.ansible_api_v2 import ANSRunner
from safe.Helper import  SQL_db
from django.forms.models import model_to_dict

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_assets_list(request,format=None):

    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Assets.objects.filter(admin_user_id=request.user.id).count()
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
                assets_values_list = Assets.objects.filter(
                    Q(admin_user_id=request.user.id) |
                    Q(assets_ip=search)

                ).values_list(
                    'id',
                    'assets_ip',
                    'assets_status',
                    'assets_name',
                    'assets_hostname',
                    'assets_allip',
                    'assets_region',
                    'assets_business',
                    'assets_os',
                    'assets_who',
                    'create_date'
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                print search
                search_list = Assets.objects.filter(
                    Q(admin_user_id=request.user.id) and
                    Q(assets_ip__contains=search)|
                    Q(assets_status__contains=search)|
                    Q(assets_type__contains=search)|
                    Q(assets_business__business_name__contains=search)|
                    Q(assets_region__contains=search)


                ).values_list(
                    'id',
                    'assets_ip',
                    'assets_status',
                    'assets_name',
                    'assets_hostname',
                    'assets_allip',
                    'assets_region',
                    'assets_business',
                    'assets_os',
                    'assets_who',
                    'create_date'
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)

            all_list = []
            for i in all_lists:
                i[2] = Assets.objects.get(assets_status=i[2], id=i[0]).get_assets_status_display()
                i[7] = Business_group.objects.filter(id=i[7]).values_list('business_name', flat=True)[0]
                i[10]=(i[10]).strftime('%Y-%m-%d %H:%M:%S')
                print i[10]
                print type(i[10])
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))
    elif request.method == 'POST':
        if(request.data.get('data')):
            data =  request.data.get('data')
            data['admin_user_id']=request.user.id
            data['portpass_tgthost'] = ','.join(data["portpass_tgthost"])
            print request.user.id
        else:
            data = request.data
        #print  data
        serializer = Portpass_task_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(23, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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
def run_assets_asnible(request, id, format=None):
    if request.method == 'GET':
            server_assets=Server_Assets.objects.get(assets_id=id)
            if server_assets.username=='' and server_assets.passwd='':
            resource = [
                {"hostname": server_assets.hostname, "port": server_assets.port, "username": server_assets.username,
                 "password": server_assets.passwd}]
            ANS= ANSRunner(resource)
            ANS.run_model(host_list=[server_assets.hostname], module_name='setup', module_args="")
            assets_info = ANS.handle_cmdb_data(ANS.get_model_result())
            assets_network = ANSRunner(resource)
            assets_process= ANSRunner(resource)
            assets_user= ANSRunner(resource)
            assets_network.run_model(host_list=[server_assets.hostname], module_name='shell', module_args="netstat -tlnp")
            assets_process.run_model(host_list=[server_assets.hostname], module_name='shell', module_args="ps -aux")
            assets_user.run_model(host_list=[server_assets.hostname], module_name='shell', module_args="cat /etc/passwd")
            assets_network = assets_network.get_model_result()
            print assets_user
            assets_process = assets_process.get_model_result()
            assets_user = assets_user.get_model_result()
            SQL_db.assets_ansible(id,assets_info,assets_network,assets_process,assets_user,request.user.id,server_assets.hostname)
            return HttpResponse('200', status=200)

    else:
            return HttpResponse('200', status=200)

@api_view([ 'GET', 'POST',])
@csrf_exempt
def get_host_process(request,id,format=None):
    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Assets_Host_Process.objects.filter(assets_id=id).count()
            draw = int(request.GET.get('draw'))
            start = int(request.GET.get('start'))  # 从多少行开始
            length = int(request.GET.get('length'))  # 显示多少条数据
            end = start + length  # 到多少行结束
            if search == "":
                assets_values_list = Assets_Host_Process.objects.filter(
                    assets_id=id
                ).values_list(
                    'id',
                    'user',
                    'pid',
                    'cpu',
                    'men',
                    'rss',
                    'stat',
                    'time',
                    'command',
                    'update_date'
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                print search
                search_list =Assets_Host_Process.objects.filter(
                    Q( assets_id=id) and
                    Q(user__contains=search)|
                    Q(pid__contains=search)|
                    Q(update_date__contains=search)|
                    Q(stat__contains=search)|
                    Q(command__contains=search)

                ).values_list(
                    'id',
                    'user',
                    'pid',
                    'cpu',
                    'men',
                    'rss',
                    'stat',
                    'time',
                    'command',
                    'update_date'
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)

            all_list = []
            for i in all_lists:
                i[9]=(i[9]).strftime('%Y-%m-%d %H:%M:%S')
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))

@api_view([ 'GET', 'POST',])
@csrf_exempt
def get_host_user(request,id,format=None):
    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Assets_Host_User.objects.filter(assets_id=id).count()
            draw = int(request.GET.get('draw'))
            start = int(request.GET.get('start'))  # 从多少行开始
            length = int(request.GET.get('length'))  # 显示多少条数据
            end = start + length  # 到多少行结束
            if search == "":
                assets_values_list = Assets_Host_User.objects.filter(
                    assets_id=id
                ).values_list(
                    'id',
                    'user',
                    'ps',
                    'uid',
                    'gid',
                    'user_name',
                    'home',
                    'shell',
                    'update_date'
                ).order_by('-id')[start: end]
                _filter = asset_count
                all_lists = map(list, assets_values_list)
            else:
                print search
                search_list =Assets_Host_User.objects.filter(
                    Q( assets_id=id) and
                    Q(user__contains=search)|
                    Q(ps__contains=search)|
                    Q(user_name__contains=search)|
                    Q(home__contains=search)|
                    Q(shell__contains=search)

                ).values_list(
                    'id',
                    'user',
                    'ps',
                    'uid',
                    'gid',
                    'user_name',
                    'home',
                    'shell',
                    'update_date'
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)

            all_list = []
            for i in all_lists:
                i[8]=(i[8]).strftime('%Y-%m-%d %H:%M:%S')
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))

@api_view([ 'GET', 'POST',])
@csrf_exempt
def get_host_vul(request,id, format=None):
    if request.method == 'GET':
        search = request.GET.get('search[value]')
        draw = int(request.GET.get('draw'))
        start = int(request.GET.get('start'))  # 从多少行开始
        length = int(request.GET.get('length'))  # 显示多少条数据
        end = start + length  # 到多少行结束
        vul_objects = Host_vul.objects.filter(assets_ip_id=id)
        if search == "":
            recordsTotal = vul_objects.count()
            recordsFiltered = recordsTotal
            objects = vul_objects[start:end]
            dic = [model_to_dict(obj) for obj in objects]

        else:
            print search
            vul_objects=vul_objects.filter(
                Q(vul_name__contains=search) |
                Q(vul_cve__contains=search) |
                Q(vul_port__contains=search) |
                Q(vul_server__contains=search) |
                Q(vul_category__contains=search)
            )
            recordsTotal = vul_objects.count()
            recordsFiltered = recordsTotal
            objects = vul_objects[start:end]
            dic = [model_to_dict(obj) for obj in objects]
        for item in dic:
            item['create_date']=item['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        print   dic
        data = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsTotal,
            'data': dic
        }

        return HttpResponse(json.dumps(data))




