#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/28 下午1:22
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : view.py
# @Software: PyCharm
#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from django.contrib.auth.decorators import login_required
from  models import  *
from system_config.models import  *
from tasks import  *
from safe.Helper.pager import Pagination
from safe.Helper import   cron_tasks
import  xlrd
import  time
from django.conf import settings

@login_required
def index(request):
    error = Log.objects.filter(log_level=3).order_by('-create_date')
    navigations = Navigation.objects.all()
    sub_navigations=Sub_navigation.objects.all()
    return render(request, 'index.html',locals())

def weclome(request):

    return  render(request,'welcome.html',locals())


def  logx(request):
    navigations = Navigation.objects.all()
    sub_navigations = Sub_navigation.objects.all()
    log=Log.objects.filter(admin_user_id=request.user.id).order_by('-create_date')
    max = len(log)
    current_page = request.GET.get('p')
    print current_page
    name='logx'
    page_obj = Pagination(max,current_page,name)
    data = log[page_obj.start():page_obj.end()]
    return render( request, 'log.html', locals())


def test(request):
    try:
        wb = xlrd.open_workbook('/root/web/safe/assets.xls')  # 关键点在于这里
        table = wb.sheets()[0]
        row = table.nrows
        for i in xrange(1, row):
            col = table.row_values(i)
            assets_business=col[3]
            print type(assets_business)
            print col
            if col[0]=='':continue
            if  assets_business=='':assets_business='未知'
            if  col[4]=='':
                assets_who='未知'
                assets_tel='未知'
            else:
                assets_tel = col[4].split(' ')[1]
                assets_who = col[4].split(' ')[0]



            if  Business_group.objects.filter(business_name=assets_business).exists():
                assets_business_id=Business_group.objects.get(business_name=assets_business).id
                if Assets.objects.filter(assets_name='运维平台',server_pic_id=1,admin_user_id=request.user.id,
                                      assets_ip=col[0],assets_allip=col[1],assets_region=col[2],
                                      assets_who=assets_who,assets_tel=assets_tel,
                                      assets_business_id=assets_business_id,
                                      assets_hostname='未知',).exists():
                             pass
                else:
                    assets_obj=Assets.objects.create(assets_name='运维平台',server_pic_id=1,admin_user_id=request.user.id,
                                          assets_ip=col[0],assets_allip=col[1],assets_region=col[2],
                                          assets_who=assets_who,assets_tel=assets_tel,
                                          assets_business_id=assets_business_id,
                                          assets_hostname='未知',
                                         )
                    Server_Assets.objects.create(assets=assets_obj, hostname=col[0])
            else:
                if Assets.objects.filter(assets_name='运维平台', server_pic_id=1, admin_user_id=request.user.id,
                                         assets_ip=col[0], assets_allip=col[1], assets_region=col[2],
                                         assets_who=assets_who, assets_tel=assets_tel,
                                         assets_business_id=assets_business_id,
                                         assets_hostname='未知', ).exists():
                    pass
                else:
                   Business_group.objects.create(business_name=assets_business,admin_user_id=request.user.id)
                   assets_business_id = Business_group.objects.get(business_name=assets_business).id
                   assets_obj=Assets.objects.create(assets_name='运维平台', server_pic_id=1, admin_user_id=request.user.id,
                                         assets_ip=col[0], assets_allip=col[1], assets_region=col[2],
                                         assets_who=assets_who, assets_tel=assets_tel,
                                         assets_business_id=assets_business_id,
                                         assets_hostname='未知',
                                         )
                   Server_Assets.objects.create(assets=assets_obj, hostname=col[0])


    except Exception as e:
        print e
    return HttpResponse('200', status=200)



def tools(request):
    tools_info=Server_docker.objects.all()
    return render(request, 'tools.html', locals())

