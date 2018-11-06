#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 下午2:45
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : views.py.py
# @Software: PyCharm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response,HttpResponse
from django.contrib.auth.decorators import login_required
from  safe.models import  *
from  system_config.models import  *
from django.views.decorators.csrf import csrf_exempt
import  xlrd
import json
from safe.Helper.pager import Pagination
from django.conf import settings
@csrf_exempt
def  asset_upload(request):
    if request.method =='POST':
        try:
            wb = xlrd.open_workbook(
                filename=None, file_contents=request.FILES['file'].read())  # 关键点在于这里
            table = wb.sheets()[0]
            row = table.nrows
            for i in xrange(1, row):
                col = table.row_values(i)
                print col
                Assets.objects.create(assets_name=col[0],assets_ip=col[1],assets_url=col[2],assets_status=int(col[3]),
                                      admin_user_id=int(col[4]),  assets_business_id=int(col[5]),
                                      assets_os=col[6],
                                      assets_type=col[7],
                                      server_pic_id=int(col[8]),)
                print col
        except Exception as e:
            print e
    return  HttpResponse('200', status=200)

def  assets(request):
    error = Log.objects.filter(log_level=3).order_by('-create_date')
    navigations = Navigation.objects.all()
    sub_navigations = Sub_navigation.objects.all()
    assets_list = Assets.objects.filter(admin_user_id=request.user.id)
    business_group=Business_group.objects.filter(admin_user_id=request.user.id)
    pic_list = Pic.objects.filter(admin_user_id=request.user.id)
    max=len(assets_list)
    current_page = request.GET.get('p')
    page_obj = Pagination(max, current_page,'assets')
    data_list = assets_list[page_obj.start():page_obj.end()]
    return render(request, 'assets/assets.html', locals())

@csrf_exempt
def  add_assets(request):
     if request.method =='POST':
         try:
             ret = {'status': 1001, 'error': ''}
             data = json.loads(request.body, encoding='utf-8')
             asset=data['data']
             assets_obj=Assets.objects.create(
                    assets_ip=asset['assets_ip'],
                    assets_name=asset['assets_name'],
                    assets_type=asset['assets_type'],
                    assets_hostname=asset['assets_hostname'],
                    assets_region=asset['assets_region'],
                    assets_who=asset['assets_who'],
                    assets_tel=asset['assets_tel'],
                    assets_allip=asset['assets_allip'],
                    assets_url=asset['assets_url'],
                    assets_os=asset['assets_os'],
                    assets_business_id=int(asset['assets_group']),
                    server_pic_id=int(asset['assets_pic']),
                    admin_user_id=request.user.id,
                    assets_status=2
                     )

             Server_Assets.objects.create(assets=assets_obj,hostname=asset['assets_ip'])
             ret['status'] = 1002
         except Exception  as e:
             ret['error'] = str(e)
         return HttpResponse(json.dumps(ret))
     else:
         return HttpResponse('200', status=500)

@csrf_exempt
def   del_assets(request):
    if request.method == 'POST':
        data = json.loads(request.body, encoding='utf-8')
        asset_id = data['data']
        for  asset_id in asset_id:
            Assets.objects.filter(id=int(asset_id)).delete()
        return HttpResponse('200', status=200)

    else:
        pass
    return HttpResponse('200', status=200)


def  host_info(request,id):
    error = Log.objects.filter(log_level=3).order_by('-create_date')
    navigations = Navigation.objects.all()
    sub_navigations = Sub_navigation.objects.all()
    assets_info=Assets.objects.filter(id=id)
    server_info=Server_Assets.objects.filter(assets_id=id)
    port_info=Asset_port.objects.filter(assets_ip_id=id)
    host_vul=Host_vul.objects.filter(assets_ip_id=id)
    pass_info=Asset_pass.objects.filter(assets_ip_id=id)
    ansible_network=Assets_Host_Network.objects.filter(assets_id=id)
    for i  in assets_info:
        print i
    assets_id=id
    print assets_id
    return render(request, 'assets/host_info.html',locals())
