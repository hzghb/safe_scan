#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 下午5:22
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : port_api.py.py
# @Software: PyCharm

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
from rest_framework.views import APIView
from django.shortcuts import render,render_to_response,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from safe import  tasks
from  safe.tasks  import *
from django.db.models import Q
from safe.Helper import Checkip
from djcelery.models import  *
from celery.result import AsyncResult
from safe.Helper import  nsfocus
from safe.Helper import  SQL_db
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_brute_task(request,format=None):
    if request.method == 'GET':
        search = request.GET.get('search[value]')
        draw = int(request.GET.get('draw'))
        start = int(request.GET.get('start'))  # 从多少行开始
        length = int(request.GET.get('length'))  # 显示多少条数据
        end = start + length  # 到多少行结束
        brute_objects = Brute_task.objects.filter(admin_user_id=request.user.id)
        if search == "":
            recordsTotal = brute_objects.count()
            recordsFiltered = recordsTotal
            objects = brute_objects[start:end]
            dic = [model_to_dict(obj) for obj in objects]

        else:
            print search
            brute_objects=brute_objects.filter(
                Q(breute_name__contains=search)
            )
            recordsTotal = brute_objects.count()
            recordsFiltered = recordsTotal
            objects = brute_objects[start:end]
            dic = [model_to_dict(obj) for obj in objects]
        for  item in dic:
            item['admin_user']=Brute_task.objects.get(id=item['id']).admin_user.username
        data = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsTotal,
            'data': dic
        }

        return HttpResponse(json.dumps(data))


@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def  add_brute_task(request,format=None):
 if request.method == 'POST':
        ret = {'code': 1001, 'data': '', 'msg': ''}
        try:
            if(request.data.get('data')):
                data =  request.data.get('data')
                Brute_task.objects.create(admin_user_id=request.user.id,brute_tgthost=str(data['brute_tgthost'])
                                          ,brute_user=data['brute_user'],brute_userdic=data['brute_userdic'],
                                           brute_passdic=data['brute_passdic'],brute_threding=int(data['brute_threding']),
                                           brute_models=data['brute_models'],
                                           brute_name=data['brute_name']
                                          )
            ret['msg']='添加任务成功'

        except Exception as e:
            ret['msg']=str(e)
            ret['code']=1002
        return JsonResponse(ret)




@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def del_brute_task(request,format=None):
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
def start_brute_task(request,id, format=None):
    ret = {'code': 1001, 'data': '', 'msg': ''}
    if request.method == 'GET':
        task_info = Brute_task.objects.get(id=id)
        if task_info.brute_status == '等待':
            assets_id_list=json.loads(task_info.brute_tgthost)
            print assets_id_list
            scanmodel= task_info.brute_models
            for assets_id in assets_id_list:
                 if  Asset_port.objects.filter(assets_ip_id=assets_id,protocal=scanmodel):
                    print assets_id
                    port=(Asset_port.objects.get(assets_ip_id=assets_id,protocal=scanmodel)).port_number
                    ip=(Assets.objects.get(id=assets_id)).assets_ip
                    task=tasks.brute_task.delay(
                                        ip=ip,
                                        username=task_info.brute_user,
                                        scanmodel=scanmodel,
                                        passfile=task_info.brute_passdic,
                                        userfile=task_info.brute_userdic,
                                        threding=task_info.brute_threding,
                                        port=str(port),
                                        assets_id=assets_id,
                                        user_id=request.user.id,
                                        task_id=id,
                                        )
                    Brute_sub_task.objects.create(sub_task_id=task.id,task_scan_id=id,ip=ip)
            return  JsonResponse(ret)

        elif task_info.brute_status == '进行中':
            ret['code'] = 1002
            ret['msg'] = '任务正在运行中'
            return JsonResponse(ret)

        else:
            ret['code'] = 1003
            ret['msg'] = '任务重新开始吗'
            return JsonResponse(ret)



@api_view([ 'GET', 'POST',])
@csrf_exempt
def restart_brute_task(request,id, format=None):
    ret = {'code': 1001, 'data': '', 'msg': ''}
    if request.method == 'GET':
        Brute_task.objects.filter(id=id).update(brute_status='等待')
        task_info = Brute_task.objects.get(id=id)
        Scan_pass.objects.filter(task_scan_id=id).delete()
        Brute_sub_task.objects.filter(task_scan_id=id).delete()
        if task_info.brute_status == '等待':
            assets_id_list=json.loads(task_info.brute_tgthost)
            print assets_id_list
            scanmodel= task_info.brute_models
            for assets_id in assets_id_list:
                 if  Asset_port.objects.filter(assets_ip_id=assets_id,protocal=scanmodel):
                    print assets_id
                    port=(Asset_port.objects.get(assets_ip_id=assets_id,protocal=scanmodel)).port_number
                    ip=(Assets.objects.get(id=assets_id)).assets_ip
                    task=tasks.brute_task.delay(
                                        ip=ip,
                                        username=task_info.brute_user,
                                        scanmodel=scanmodel,
                                        passfile=task_info.brute_passdic,
                                        userfile=task_info.brute_userdic,
                                        threding=task_info.brute_threding,
                                        port=str(port),
                                        assets_id=assets_id,
                                        user_id=request.user.id,
                                        task_id=id,
                                        )
                    Brute_sub_task.objects.create(sub_task_id=task.id,task_scan_id=id,ip=ip)
            return  JsonResponse(ret)



@api_view([ 'GET', 'POST',])
@csrf_exempt
def get_sub_brute_task(request, id, format=None):
    if request.method == 'GET':
        search = request.GET.get('search[value]')
        asset_count = Brute_sub_task.objects.filter(task_scan_id=id).count()
        draw = int(request.GET.get('draw'))
        start = int(request.GET.get('start'))  # 从多少行开始
        length = int(request.GET.get('length'))  # 显示多少条数据
        end = start + length  # 到多少行结束
        if search == "":
            assets_values_list =Brute_sub_task.objects.filter(
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
def get_sub_brute_info(request,id,format=None):

    if request.method == 'GET':
            search = request.GET.get('search[value]')
            asset_count =Scan_pass.objects.filter(admin_user_id=request.user.id,task_scan_id=id).count()
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
                assets_values_list =Scan_pass.objects.filter(
                    Q(admin_user_id=request.user.id) ,
                    Q(task_scan_id=id)



                ).values_list(
                    'id',
                    'ip',
                    'port',
                    'username',
                    'password',
                    'type',
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
                    'port',
                    'username',
                    'password',
                    'type',
                    'create_date',
                ).order_by('-id')[start: end]

                _filter = len(search_list)
                all_lists = map(list, search_list)
                print all_lists

            all_list = []
            for i in all_lists:
                i[6]=(i[6]).strftime('%Y-%m-%d %H:%M:%S')
                all_list.append(i)

            data = {
                'draw': draw,
                'recordsTotal': asset_count,
                'recordsFiltered': _filter,
                'data': all_list
            }

            return HttpResponse(json.dumps(data))



