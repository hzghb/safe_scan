#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 下午4:23
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : api_url.py
# @Software: PyCharm
from django.conf.urls import url
from django.contrib import admin
from  safe.login.view  import   *
from safe.url import  *
from safe.restfull import  port_api ,nsfocus_api,assets_api,log_api,brute_api,tree_assets_api

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error
urlpatterns = [

    #资产任务扫描信息
    url(r'^get/assets/host_list',assets_api.get_assets_list),
    url(r'^run_assets_asnible/(?P<id>[0-9]+)/$', assets_api.run_assets_asnible),
    url(r'^get/host/process/(?P<id>[0-9]+)/$', assets_api.get_host_process),
    url(r'^get/host/user/(?P<id>[0-9]+)/$',    assets_api.get_host_user),
    url(r'^get/host/vul/(?P<id>[0-9]+)/$',  assets_api.get_host_vul),

    #端口任务扫描信息
    url(r'^get/port/task_list/', port_api.get_port_task),
    url(r'^add/port/task/', port_api.add_port_task),
    url(r'^del/port/task/', port_api.del_port_task),
    url(r'^start/port/task/(?P<id>[0-9]+)/$', port_api.port_start_task),
    url(r'^restart/port/task/(?P<id>[0-9]+)/$', port_api.port_restart_task),
    url(r'^get/sub_port_task/(?P<id>[0-9]+)/$', port_api.get_sub_port_task),
    url(r'^get/sub_port_info/(?P<id>[0-9]+)/$', port_api.get_sub_port_info),

    #弱口令扫描任务
    url(r'^get/brute/task_list/', brute_api.get_brute_task),
    url(r'^add/brute/task/', brute_api.add_brute_task),
    url(r'^del/brute/task/', brute_api.del_brute_task),
    url(r'^start/brute/task/(?P<id>[0-9]+)/$',brute_api.start_brute_task),
    url(r'^restart/brute/task/(?P<id>[0-9]+)/$',brute_api.restart_brute_task),
    url(r'^get/sub_brute_task/(?P<id>[0-9]+)/$', brute_api.get_sub_brute_task),
    url(r'^get/sub_brute_info/(?P<id>[0-9]+)/$', brute_api.get_sub_brute_info),


    #绿盟任务信息
    url(r'^get/nsfcous/task_list/',nsfocus_api.get_nsfocus_task),
    url(r'^add/nsfocus/task/',nsfocus_api.add_nsfocus_task),
    url(r'^del/nsfocus/task/', nsfocus_api.del_nsfocus_task),
    url(r'^start/nsfoucs/task/(?P<id>[0-9]+)/$',nsfocus_api.start_nsfocus_task),
    url(r'^get/nsfocus/report/(?P<id>[0-9]+)/$', nsfocus_api.get_nsfocus_report),
    url(r'^get/tree_assets_info/',tree_assets_api.get_tree_assets),



    #日志
    url(r'^get_log', log_api.get_log),

    ##ansible


]