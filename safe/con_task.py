#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 上午11:27
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : contab_task.py
# @Software: PyCharm
from safe.Helper import nsfocus
from safe.models import  *
from system_config.models import  *
from djcelery.models import  *
import  json
import os
from django.forms.models import model_to_dict
def  get_cpu():
    nsfocus_dev_obj=Nsfoucs_Scan_dev.objects.all()
    for item in nsfocus_dev_obj:
        work_init= nsfocus.Work(item.address,item.user,item.passwd)
        try:
          cpu =int(work_init.sys__status()['cpu'])
          if cpu<30:
              nsfocus_task= Nsfocus_task.objects.filter(nsfocus_status=8,nsfocus_dev=item.id)[0]
              print nsfocus_task.nsfocus_tgthost
              assets_list=json.loads(nsfocus_task.nsfocus_tgthost)
              print assets_list
              print type(assets_list)
              iplist=get_tgthost(assets_list)
              work_init.create_xml(targets=iplist, taskname=nsfocus_task.nsfocus_name,
                             live=nsfocus_task.nsfocus_active, port_strategy_userports=nsfocus_task.nsfocus_port,
                             port_speed=str(nsfocus_task.nsfocus_port_level), scan_level=str(nsfocus_task.nsfocus_level)

                             )
              result=work_init.addtask()
              result=json.loads(result)
              print result['ret_msg']
              if result['ret_msg'] == 'success':
                  task_id = result['data']['task_id']
                  Nsfocus_task.objects.filter(id=nsfocus_task.id).update(nsfocus_status=2, nsfocus_task_id=int(task_id))
              else:
                  print '参数有误'
        except Exception as e:
             print '服务器不能正常连接'
             print e
    print cpu

def  get_tgthost(assets_list):
     iplist=''
     for id in  assets_list:
        iplist=iplist+(Assets.objects.get(id=id)).assets_ip+';'
     return  iplist




############ping扫描#############################
def get_ping_host():
    try:
        assets_list=Assets.objects.all()
        f = open('ip.txt', 'a')
        for ip in assets_list:
            f.writelines(ip.assets_ip+'\n')
        f.close()
    except Exception as e:
        print e
    return  'ok'


def run_ping():
    try:
        os.system('rm -rf  ip.txt')
    except Exception as e:
        print  e
    print '任务开始'
    iplist=get_ping_host()
    cmd='nmap -i ip.txt -v -sn -PE -PN -n --min-hostgroup 1024 --min-parallelism 1024 -oX nmap_ping.xml'
    print  cmd
    y=os.system(cmd)
    ping_list('nmap_ping.xml')


def ping_list (filename):
    import xml.etree.ElementTree as ET
    up_list=[]
    ip_list=[]
    tree = ET.ElementTree(file=filename)
    for elem in tree.iter(tag='address'):
        ip_list.append(elem.attrib['addr'])
    for elem in tree.iter(tag='status'):
        up_list.append(elem.attrib['state'])
    info=dict(zip(ip_list, up_list))
    for  ip, status in info.items():
         if status=='up':Assets.objects.filter(assets_ip=ip).update(assets_status=0)
         else: Assets.objects.filter(assets_ip=ip).update(assets_status=1)
    return   'ok'



def listing_port_task():
    try:
        print '开始'
        port_info=Portpass_task.objects.all()
        for obj in  port_info:
            objects=Sub_task.objects.filter(task_scan_id=obj.id)
            if objects:
                code = 0
                for sub in objects:
                     state=TaskState.objects.get(task_id=sub.sub_task_id).state
                     if state=='PENDING' or  state=='RECEIVED' or state=='STARTED':
                          code=code+1
                print code
                if code==0:
                     Portpass_task.objects.filter(id=obj.id).update(portpass_status=4)
                print '结束'
            else:
                return 'ok'
    except Exception as e:
         print  e
    return  'ok'



def listing_brute_task():
    try:
        print '开始'
        brute_info=Brute_task.objects.all()
        for obj in  brute_info:
            objects=Brute_sub_task.objects.filter(task_scan_id=obj.id)
            if objects:
                code = 0
                for sub in objects:
                     state=TaskState.objects.get(task_id=sub.sub_task_id).state
                     if state=='PENDING' or  state=='RECEIVED' or state=='STARTED':
                          code=code+1
                print code
                if code==0:
                     Brute_task.objects.filter(id=obj.id).update(brute_status='完成')
                print '结束'
            else:
                return 'ok'
    except Exception as e:
         print  e
    return  'ok'








