#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/23 下午3:07
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : Checkip.py
# @Software: PyCharm
import re
from safe.models import  *
def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def iplist(active,tgtlist=[],):
     iplist=[]
     for tgthost in tgtlist:
         if checkip(tgthost)==True:
            iplist.append(tgthost)
         else:
           asset_ip=Assets.objects.filter(assets_business__business_name=tgthost)
           for obj in asset_ip:
              if active == 'on':
                try:
                 obj.asset_pass_set.all().delete()
                 obj.asset_port_set.all().delete()
                except  Exception as e:
                    print  e
              else:
                  pass
              iplist.append(obj.assets_ip)
     return  iplist









