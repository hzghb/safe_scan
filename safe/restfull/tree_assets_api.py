#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 下午9:25
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : tree_assets_api.py.py
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
from safe import  tasks
from  safe.tasks  import *
from django.db.models import Q
from safe.Helper import Checkip
from djcelery.models import  *
from celery.result import AsyncResult
from safe.Helper import  nsfocus
from safe.Helper import  SQL_db
from django.conf import settings

@api_view(['GET', 'POST','DELETE' ])
@csrf_exempt
def get_tree_assets(request,format=None):
    if request.method == 'GET':
       group_tree=[]
       assets_group=Business_group.objects.filter(admin_user_id=request.user.id)
       for item in assets_group:
           business={'children':[],'id':item.id,'name':item.business_name}
           assets_info=Assets.objects.filter(assets_business_id=item.id)
           for assets in assets_info:
                assets_group={'id':assets.id,'name':assets.assets_ip}
                business['children'].append(assets_group)
           group_tree.append(business)
       return HttpResponse(json.dumps(group_tree))

