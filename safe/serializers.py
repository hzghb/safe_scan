#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 上午10:36
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : serializers.py.py
# @Software: PyCharm

from rest_framework import serializers
from  safe.models import  *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username',
                  'first_name','last_name','email','is_staff',
                  'is_active','date_joined')

class Portpass_task_Serializer(serializers.ModelSerializer):
    admin_user_id= serializers.IntegerField()

    class Meta:
        model = Portpass_task
        fields = ( 'portpass_tgthost','portpass_name','portpass_port',
                   'portpass_active',
                   'admin_user_id',
                   )


class  Nsfocus_task_Serializer(serializers.ModelSerializer):
    admin_user_id= serializers.IntegerField()
    nsfocus_level=serializers.IntegerField()
    nsfocus_port_level=serializers.IntegerField()
    class Meta:
        model = Nsfocus_task
        fields = ('nsfocus_tgthost', 'nsfocus_name', 'nsfocus_desc', 'nsfocus_level', 'nsfocus_dev',
                  'nsfocus_port_level', 'nsfocus_port', 'nsfocus_active', 'admin_user_id'
                  )
