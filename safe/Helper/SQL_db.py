#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 上午9:05
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : Sql_db.py.py
# @Software: PyCharm
from  safe.models import  *
from  safe.Helper import log
from host_db import *
import log

def  os_port_db(assets_id,ip,port,task_id,user_id,servicename,serviceversion):
    Asset_port.objects.filter(port_number=port,assets_ip_id=assets_id).update(protocal=servicename,banner=serviceversion)
    Scan_port.objects.filter(port_number=port,admin_user_id=user_id,ip=ip,task_scan_id=task_id).update(protocal=servicename,banner=serviceversion)
    return  'ok'



def  port_db(assets_id,ip,port,task_id,user_id,):
            if Asset_port.objects.filter(port_number=port, assets_ip_id=assets_id):
                Asset_port.objects.filter(port_number=port, assets_ip_id=assets_id).update()
            else:
                Asset_port.objects.create(port_number=port,state=0,assets_ip_id=assets_id,)
            Scan_port.objects.create(port_number=port,admin_user_id=user_id,ip=ip,task_scan_id=task_id)
            return 'ok'


def   pass_db(ip,username,password,scanmodel,port,assets_id,task_id,user_id ):
      try:

          if Asset_pass.objects.filter(username=username,password=password,type=scanmodel,port=int(port),assets_ip_id=assets_id,admin_user_id=user_id):
              Asset_pass.objects.filter(username=username, password=password, type=scanmodel,port=int(port),assets_ip_id=assets_id,admin_user_id=user_id).update(status=1)
          else:
              Asset_pass.objects.create(username=username, password=password, type=scanmodel, port=int(port),assets_ip_id=assets_id,admin_user_id=user_id,status=1)
              content = '发新了弱口令用户为%s,密码为%s,类型为%s' % (username, password, scanmodel)
              log.brute_info(ip, content.decode('utf-8'), user_id, 3)
          Scan_pass.objects.create(ip=ip, port=int(port), username=username, password=password,type=scanmodel,task_scan_id=task_id, admin_user_id=user_id )
          content='更新了弱口令扫描信息'
          log.brute_info(ip, content.decode('utf-8'), user_id, 1)
          return  'ok'
      except Exception as e:
          print  e



def vul_db(id,nsfocus_task_id,result,admin_user_id):
    for item  in result:
         ip=item['ip']
         print "**************************************"
         print  ip
         for  vul  in item['vuln_detail']:
             for scan in item['vuln_scanned']:
                 if  vul['vul_id']==scan['vul_id']:
                     try:
                        assets_id = (Assets.objects.get(assets_ip=ip)).id
                        id=int(id)
                        if  7.0<=vul['risk_points']<=10.0:
                                vul_level=0
                        elif 5.0<=vul['risk_points']<7.0:
                               vul_level = 1
                        elif 2.0<=vul['risk_points']<5.0:
                               vul_level = 2
                        else:
                             vul_level=3


                        if  Host_vul.objects.filter(ip=ip,vul_name=vul['name'], vul_desc=vul['description']).exists():
                                 Host_vul.objects.filter(ip=ip,vul_name=vul['name'], vul_desc=vul['description']).update()
                        else:
                            content = '发现了一个新的漏洞名为%s' % (vul['name'])
                            log.nsfocus_info(ip=ip, content=content, user_id=admin_user_id, log_level=3)
                            Host_vul.objects.create(
                                                    assets_ip_id=assets_id,
                                                    ip=ip,
                                                    nsfocus_task_id=id,
                                                    vul_name=vul['name'],
                                                    vul_desc=vul['description'],
                                                    vul_solution=vul['solution'],
                                                    vul_cve=vul['cve_id'],
                                                    vul_category=vul['threat_category'],
                                                    vul_app_category=vul['application_category'],
                                                    vul_mess_string=scan['mess_string'],
                                                    vul_port=str(scan['port']),
                                                    vul_protocol=scan['protocol'],
                                                    vul_server=scan['service'],
                                                    vul_status=1,
                                                    vul_level=vul_level,
                                                    admin_user_id=admin_user_id
                                                 )
                     except Exception as  e:
                          print  "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                          print e

                 else:
                     pass
             pass
         log.nsfocus_info(ip=ip, content='更新了一条主机漏洞信息', user_id=admin_user_id, log_level=0)



def  assets_ansible(id,assets_info,assets_network,assets_process,assets_user,admin_user,ip):
    print assets_info
    for  server_info in assets_info:
        Server_Assets.objects.filter(assets_id=id).update(cpu_number=server_info.get('cpu_number'),
                                                          kernel=server_info.get('kernel'),
                                                          selinux=server_info.get('selinux'),
                                                          system=server_info.get('system'),
                                                          cpu=server_info.get('cpu'),
                                                          disk_total=server_info.get('disk_total'),
                                                          cpu_core=server_info.get('cpu_core'),
                                                          swap=server_info.get('swap'),
                                                          ram_total=server_info.get('ram_total'),
                                                          vcpu_number=server_info.get('vcpu_number'),
                                                          sn = server_info.get('serial'),
                                                          model =server_info.get('model'),
                                                          manufacturer =server_info.get(
                                                            'manufacturer')

                                                          )
    host_user(assets_user,id,admin_user,ip)
    host_network(assets_network,id,admin_user,ip)
    host_process(assets_process,id,admin_user,ip)
