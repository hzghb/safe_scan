#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import  uuid
import django.utils.timezone as timezone
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

#管理员邮箱配置
class Email_Config(models.Model):
    site = models.CharField(max_length=100,verbose_name='部署站点')
    host = models.CharField(max_length=100,verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100,verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100,verbose_name='发送用户密码')
    subject = models.CharField(max_length=100,verbose_name='发送邮件主题标识',default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表',blank=True,null=True)
    class Meta:
        verbose_name_plural = '邮箱配置'

    def __str__(self):
        return '邮箱配置'




class 	Navigation(models.Model):
    status = (
        (0, '首页'),
        (1, '不是首页'),
    )
    name= models.CharField(max_length=100, verbose_name='名称')
    herf= models.CharField(max_length=100, verbose_name='连接地址')
    ico = models.CharField(max_length=100, verbose_name='图标')
    index = models.IntegerField(default=999, verbose_name='分类的排序')
    status = models.SmallIntegerField(choices=status, verbose_name='首页', default=None)

    class Meta:
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


class Sub_navigation(models.Model):
    navigation = models.ForeignKey(Navigation)
    name = models.CharField(max_length=100, verbose_name='名称')
    herf = models.CharField(max_length=100, verbose_name='连接地址')
    index = models.IntegerField(default=999, verbose_name='分类的排序')
    class Meta:
        verbose_name_plural = '子菜单'
        ordering = ['index', 'id']
    def __unicode__(self):
       return  self.name

#扫描器配置
class Nsfoucs_Scan_dev(models.Model):
    name= models.CharField(max_length=100,verbose_name='扫描器名称')
    address = models.CharField(max_length=100,verbose_name='扫描器地址')
    user= models.CharField(max_length=100,verbose_name='用户名')
    passwd = models.CharField(max_length=100,verbose_name='密码')
    class Meta:
        verbose_name_plural = '绿盟扫描器配置'

    def __unicode__(self):
       return  self.name
