#coding:utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models  import  Group
from django.db import models
import  uuid
import django.utils.timezone as timezone

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

#系统用户
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='用户头像')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    abstract=models.CharField(max_length=400,verbose_name='描述')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username

# 机房
class Pic(models.Model):
        admin_user = models.ForeignKey(User)
        name = models.CharField(max_length=50, verbose_name='名称', default='')
        address = models.CharField(max_length=100, verbose_name='机房地址', default='')
        tel = models.CharField(max_length=50, verbose_name='手机号', default='')
        create_date = models.DateTimeField(auto_now_add=True)
        update_date = models.DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name = '机房信息表'
            verbose_name_plural = verbose_name

        def __unicode__(self):
            return self.name


#资产标签
class Tag(models.Model):
    name = models.CharField( max_length=32, unique=True,verbose_name='标签表')
    class Meta:
        verbose_name_plural = "资产标签表"
    def __unicode__(self):
        return self.name



#资产业务组
class Business_group(models.Model):
    '''业务分组表'''
    admin_user = models.ForeignKey(User)
    business_name = models.CharField(max_length=50,verbose_name='业务组名称' )
    contact = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系人')
    tel = models.CharField(max_length=50, verbose_name='手机号',blank=True, null=True)
    e_mail = models.EmailField(verbose_name='邮箱', null=True,blank=True)
    class Meta:
        verbose_name_plural = '业务分组'
    def __unicode__(self):
        return u'%s %s' % (self.business_name, self.contact)


class Assets(models.Model):
    STATUS = (
        (0,'存活'),
        (1,'死亡'),
        (2,'未知'),
    )
    admin_user= models.ForeignKey(User)
    assets_ip = models.GenericIPAddressField(verbose_name='管理IP')
    assets_name = models.CharField(max_length=100,verbose_name='资产名称')
    assets_type = models.CharField(max_length=100,verbose_name='资产类型')
    assets_hostname= models.CharField(max_length=100, verbose_name='资产主机名', blank=True, null=True, default='none')
    assets_region= models.CharField(max_length=100, verbose_name='所属域',blank=True, null=True,default='none')
    assets_who= models.CharField(max_length=100, verbose_name='资产责任人', blank=True, null=True, default='none')
    assets_tel= models.CharField(max_length=100, verbose_name='联系电话', blank=True, null=True, default='none')
    assets_allip=models.CharField(max_length=600,verbose_name='所有IP',blank=True,null=True,default='none')
    assets_url = models.CharField(max_length=100,verbose_name='资产url',null=True, blank=True)
    server_pic= models.ForeignKey('Pic',verbose_name='机房')
    assets_business = models.ForeignKey('Business_group',verbose_name='业务组')
    assets_os=models.CharField(max_length=100,verbose_name='操作系统os')
    create_date = models.DateTimeField('创建日期',default=timezone.now)
    update_date = models.DateTimeField('最后修改日期',auto_now=True)
    assets_status = models.IntegerField(choices=STATUS, default=2, verbose_name='资产状态')
    class Meta:
        verbose_name_plural = '资产信息库'

    def __unicode__(self):
        return u'%s %s' % (self.assets_name ,self.assets_ip)

class Server_Assets(models.Model):
    assets = models.OneToOneField('Assets')
    hostname = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    passwd = models.CharField(max_length=100, blank=True, null=True)
    port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    cpu_number = models.SmallIntegerField(blank=True, null=True)
    vcpu_number = models.SmallIntegerField(blank=True, null=True)
    cpu_core = models.SmallIntegerField(blank=True, null=True)
    disk_total = models.CharField(max_length=100, blank=True, null=True)
    ram_total = models.CharField(max_length=100, blank=True, null=True)
    kernel = models.CharField(max_length=100, blank=True, null=True)
    selinux = models.CharField(max_length=100, blank=True, null=True)
    swap = models.CharField(max_length=100, blank=True, null=True)
    raid = models.SmallIntegerField(blank=True, null=True)
    system = models.CharField(max_length=100, blank=True, null=True)
    sn = models.CharField(max_length=100, verbose_name='设备序列号', blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='制造商')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = '服务器资产'
    def __unicode__(self):
        return u'%s %s' % (self.hostname, self.username)


class  Assets_Host_Network(models.Model):
    assets = models.ForeignKey('Assets')
    proto= models.CharField(max_length=100, blank=True, null=True, verbose_name='接受')
    recv = models.CharField(max_length=100, blank=True, null=True, verbose_name='发送')
    send = models.CharField(max_length=100, blank=True, null=True, verbose_name='协议')
    localaddress = models.CharField(max_length=100, blank=True, null=True, verbose_name='本地地址')
    foraddress= models.CharField(max_length=100, blank=True, null=True, verbose_name='远程地址')
    status= models.CharField(max_length=100, blank=True, null=True, verbose_name='状态')
    pid = models.CharField(max_length=100, blank=True, null=True, verbose_name='进程')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = '主机网络资产'
    def __unicode__(self):
        return u'%s %s' % (self.proto, self.pid)

class  Assets_Host_Process(models.Model):
    assets = models.ForeignKey('Assets')
    user = models.CharField(max_length=100, blank=True, null=True, verbose_name='用户')
    pid = models.CharField(max_length=100, blank=True, null=True, verbose_name='进程id')
    cpu= models.CharField(max_length=100, blank=True, null=True, verbose_name='cpu使用率')
    men = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存使用率')
    vsz= models.CharField(max_length=100, blank=True, null=True, verbose_name='虚拟内存')
    rss= models.CharField(max_length=100, blank=True, null=True, verbose_name='常驻内存')
    tty= models.CharField(max_length=100, blank=True, null=True, verbose_name='终端')
    stat = models.CharField(max_length=100, blank=True, null=True, verbose_name='进程状态')
    start = models.CharField(max_length=100, blank=True, null=True, verbose_name='进程启动时间')
    time= models.CharField(max_length=100, blank=True, null=True, verbose_name='启动的分秒')
    command= models.CharField(max_length=100, blank=True, null=True, verbose_name='进程命令')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = '主机进程信息'
    def __unicode__(self):
        return u'%s %s' % (self.user, self.command)

class  Assets_Host_User(models.Model):
    assets= models.ForeignKey('Assets')
    user=models.CharField(max_length=100, blank=True, null=True, verbose_name='用户名')
    ps= models.CharField(max_length=100, blank=True, null=True, verbose_name='口令')
    uid = models.CharField(max_length=100, blank=True, null=True, verbose_name='用户标识符')
    gid= models.CharField(max_length=100, blank=True, null=True, verbose_name='组标识符')
    user_name= models.CharField(max_length=100, blank=True, null=True, verbose_name='用户名')
    home = models.CharField(max_length=100, blank=True, null=True, verbose_name='用户主目录')
    shell= models.CharField(max_length=100, blank=True, null=True, verbose_name='shell解释器')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = '主机用户'
    def __unicode__(self):
        return u'%s %s' % (self.user, self.home)















class Host_vul(models.Model):
    level = (
        (0, '高'),
        (1, '中'),
        (2, '低'),
        (3, '信息'),
    )

    STATUS = (
        (0, '已修复'),
        (1, '未修复'),
        (3,'误报'),
    )
    admin_user = models.ForeignKey(User)
    assets_ip = models.ForeignKey('Assets')
    nsfocus_task=models.ForeignKey('Nsfocus_task')
    ip=models.CharField(max_length=100,verbose_name='主机IP地址',null=True, blank=True )
    vul_name = models.CharField(max_length=100,verbose_name='漏洞名称',null=True, blank=True)
    vul_desc= models.CharField(max_length=100, verbose_name='漏洞描述', null=True, blank=True)
    vul_solution=models.TextField(verbose_name='漏洞建议',null=True, blank=True)
    vul_cve= models.CharField(max_length=100, verbose_name='漏洞CVE编号', null=True, blank=True)
    vul_category= models.CharField(max_length=100, verbose_name='漏洞分类', null=True, blank=True)
    vul_app_category= models.CharField(max_length=100, verbose_name='应用分类', null=True, blank=True)
    vul_level = models.IntegerField(choices=level, default=3, verbose_name='漏洞级别')
    vul_mess_string=models.TextField(verbose_name='漏洞返回信息',null=True, blank=True)
    vul_port= models.CharField(max_length=100, verbose_name='漏洞端口', null=True, blank=True)
    vul_protocol= models.CharField(max_length=100, verbose_name='漏洞协议', null=True, blank=True)
    vul_server= models.CharField(max_length=100, verbose_name='漏洞服务', null=True, blank=True)
    vul_status= models.IntegerField(choices=STATUS, default=1, verbose_name='漏洞状态')
    create_date = models.DateTimeField('创建日期',default=timezone.now)
    update_date = models.DateTimeField('最后修改日期',auto_now=True)
    class Meta:
        verbose_name_plural = '资产漏洞信息库'


    def __unicode__(self):
        return u'%s %s' % (self.ip, self.vul_name)





# 爆破字典
class Dic(models.Model):
    TYPE = (
        (0, '用户名'),
        (1, '密码'),
    )
    admin_user = models.ForeignKey(User)
    status = models.IntegerField(choices=TYPE, verbose_name='字典类型',null=False)
    dic_name = models.CharField(max_length=125, verbose_name='资产类型', null=False)
    dic_url=models.FileField(upload_to='dic/%Y/%m')


    class Meta:
        verbose_name_plural = '字典名称'

    def __unicode__(self):
        return self.dic_name


#密码爆破

class  Asset_pass(models.Model):
    STATUS = (
        (0, '已修复'),
        (1, '未修复'),
        (2,'误报'),
    )
    admin_user = models.ForeignKey(User)
    assets_ip=models.ForeignKey('Assets')
    port=models.IntegerField(u'')
    username=models.CharField(max_length=100,verbose_name='用户名')
    password=models.CharField(max_length=100,verbose_name='密码')
    type=models.CharField(max_length=100,verbose_name='类型')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='弱口令状态')
    class Meta:
        verbose_name_plural = '资产弱口令信息库'

    def __unicode__(self):
        return  u'%s %s' % (self.assets_ip, self.password)


#端口
class  Asset_port(models.Model):
      STATUS = (
        (0, '开启'),
        (1, '关闭'),
     )
      assets_ip=models.ForeignKey('Assets')
      port_number=models.IntegerField(verbose_name='端口号')
      state=models.IntegerField(choices=STATUS, default=0, verbose_name='端口状态')
      protocal=models.CharField(max_length=100,verbose_name='端口协议')
      banner=models.CharField(max_length=100,verbose_name='服务banner')
      create_date = models.DateTimeField(auto_now_add=True)
      update_date = models.DateTimeField(auto_now_add=True)
      class Meta:
        verbose_name_plural = '端口信息'

      def __unicode__(self):

           return self.protocal



class Scan_pass(models.Model):
    admin_user = models.ForeignKey(User)
    ip=models.CharField(max_length=100, verbose_name='IP')
    port = models.IntegerField(u'端口')
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    type = models.CharField(max_length=100, verbose_name='类型')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    task_scan = models.ForeignKey('Brute_task')

    class Meta:
        verbose_name_plural = '密码爆破'

    def __unicode__(self):
        return u'%s %s' % (self.ip, self.username)



# 端口
class Scan_port(models.Model):
  admin_user = models.ForeignKey(User)
  port_number = models.IntegerField(verbose_name='端口号')
  ip= models.CharField(max_length=100, verbose_name='IP地址')
  protocal = models.CharField(max_length=100, verbose_name='端口协议')
  banner = models.CharField(max_length=100, verbose_name='服务banner')
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now_add=True)
  task_scan = models.ForeignKey('Portpass_task')
  class Meta:
      verbose_name_plural = '端口信息'
  def __unicode__(self):
      return self.ip


#服务器DOCKER
class  Server_docker(models.Model):
    log = models.ImageField(upload_to='docker_tools/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='服务图片')
    type=models.CharField(max_length=100,verbose_name='类型')
    name=models.CharField(max_length=100,verbose_name='名称')
    url=models.CharField(max_length=100,verbose_name='URL')
    username=models.CharField(max_length=100,verbose_name='用户名')
    password=models.CharField(max_length=100,verbose_name='密码')
    class Meta:
        verbose_name_plural = '渗透环境'

    def __unicode__(self):
        return   self.name





class Log(models.Model):
    level = (
        (0, '信息'),
        (1, '中'),
        (2, '错误'),
        (3, '紧急'),
    )
    admin_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    login_ip=models.CharField(max_length=50, verbose_name='操作的主机')
    content = models.TextField(verbose_name='日志内容')
    log_level= models.IntegerField(choices=level,verbose_name='日志级别')
    log_type=models.CharField(max_length=50, verbose_name='日志类型')

    class Meta:
       verbose_name_plural = '日志告警信息'
    def __unicode__(self):
       return  self.content



class Nsfocus_task(models.Model):
    status = (
        (0, '等待'),
        (2, '运行中'),
        (5, '暂停扫描'),
        (4, '扫描完成'),
        (8, '审核中'),
    )
    scan_level= (
        (3, '普通'),
        (4, '深度'),
        (5, '极深'),
    )
    scan_port = (
        (3, '普通'),
        (4, '较快'),
        (5, '很快'),
    )
    scan_dev = (
        (0, '景芳'),
        (1, '柯桥'),
    )
    admin_user = models.ForeignKey(User)
    nsfocus_tgthost= models.CharField(max_length=1000 ,verbose_name='扫描目标',)
    nsfocus_name = models.CharField(max_length=100,verbose_name='任务名称',default=None)
    nsfocus_desc = models.CharField(max_length=200,blank=True,null=True,verbose_name='任务描述',default=None)
    nsfocus_status = models.SmallIntegerField(choices=status , verbose_name='任务状态',default=8)
    nsfocus_level = models.SmallIntegerField(choices=scan_level, verbose_name='扫描级别', default=3)
    nsfocus_dev = models.SmallIntegerField(choices=scan_dev, verbose_name='扫描器选择', default=0)
    nsfocus_port_level = models.SmallIntegerField(choices=scan_port, verbose_name='端口级别', default=3)
    nsfocus_port = models.CharField(max_length=100,verbose_name='端口范围',default='1-65535')
    nsfocus_active = models.CharField(max_length=100, verbose_name='存活判断', default='yes')
    nsfocus_task_id=models.IntegerField(verbose_name='任务结果id',blank=True, null=True)
    start_date=models.CharField(max_length=100,verbose_name='任务开始时间',blank=True, null=True)
    end_date = models.CharField(max_length=100,verbose_name='任务结束时间',blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
       verbose_name_plural = '绿盟扫描任务'

    def __unicode__(self):
       return  self.nsfocus_name



class Portpass_task(models.Model):
    status = (
        (0, '等待'),
        (2, '运行中'),
        (5, '暂停扫描'),
        (4, '扫描完成'),
    )
    admin_user= models.ForeignKey(User)
    portpass_tgthost= models.TextField(verbose_name='扫描目标',)
    portpass_name = models.CharField(max_length=100,verbose_name='任务名称',)
    portpass_port = models.CharField(max_length=100, verbose_name='端口范围', default='1-65535')
    portpass_status = models.SmallIntegerField(choices=status , verbose_name='任务状态',default=0)
    portpass_active = models.CharField(max_length=100, verbose_name='初始化配置', default='NO' , blank=True, null=True)
    start_date=models.DateTimeField(verbose_name='任务开始时间' ,blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='任务结束时间', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
       verbose_name_plural = '端口扫描'

    def __unicode__(self):
        return self.portpass_tgthost

class Brute_task(models.Model):
    admin_user = models.ForeignKey(User)
    brute_tgthost= models.TextField(verbose_name='扫描目标')
    brute_name = models.CharField(max_length=100,verbose_name='任务名称',)
    brute_status =models.CharField(max_length=100,verbose_name='任务状态',default='等待',blank=True, null=True)
    brute_user = models.CharField(max_length=1000, verbose_name='爆破用户', )
    brute_userdic=models.CharField(max_length=100, verbose_name='爆破用户字典', )
    brute_passdic=models.CharField(max_length=100, verbose_name='爆破密码字典', )
    brute_threding=models.CharField(max_length=100,verbose_name='爆破线程')
    brute_models = models.CharField(max_length=100, verbose_name='爆破模块', )
    start_date=models.DateTimeField(verbose_name='任务开始时间' ,blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='任务结束时间', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    class Meta:
       verbose_name_plural = '弱口令爆破'

    def __unicode__(self):
        return self.brute_name


#管理员邮箱配置
class Email_Config(models.Model):
    admin_user = models.ForeignKey(User)
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

class Sub_task(models.Model):
    task_scan = models.ForeignKey('Portpass_task')
    ip=models.CharField(max_length=100,verbose_name='IP地址',default='0.0.0.0')
    sub_task_id=models.CharField(max_length=100, verbose_name='子任务id')
    start_date=models.DateTimeField(verbose_name='任务开始时间', blank=True, null=True)
    end_date=models.DateTimeField(verbose_name='任务结束时间', blank=True, null=True)
    kwargs=models.TextField(verbose_name='任务参数',default='none')
    worker=models.CharField(max_length=40,verbose_name='运行的worker',default='none')
    Result=models.TextField(verbose_name='任务结果',default='none')
    class Meta:
        verbose_name_plural = '端口子任务信息'

        def __str__(self):
            return self.ip

class Brute_sub_task(models.Model):
    task_scan = models.ForeignKey('Brute_task')
    ip=models.CharField(max_length=100,verbose_name='IP地址',default='0.0.0.0')
    sub_task_id=models.CharField(max_length=100, verbose_name='子任务id')
    start_date=models.DateTimeField(verbose_name='任务开始时间', blank=True, null=True)
    end_date=models.DateTimeField(verbose_name='任务结束时间', blank=True, null=True)
    kwargs=models.TextField(verbose_name='任务参数',default='none')
    worker=models.CharField(max_length=40,verbose_name='运行的worker',default='none')
    Result=models.TextField(verbose_name='任务结果',default='none')
    class Meta:
        verbose_name_plural = '弱口令子任务信息'
        def __str__(self):
            return self.ip