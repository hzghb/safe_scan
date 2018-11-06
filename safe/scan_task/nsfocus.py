#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from safe.Helper import Checkcode
import StringIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from safe.models import    *
from system_config.models import *
from safe.Helper  import   log
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


def  task_list(request):
    error = Log.objects.filter(log_level=3).order_by('-create_date')
    assets_list = Business_group.objects.filter(admin_user_id=request.user.id)
    nsfcous_dev=Nsfoucs_Scan_dev.objects.all()
    data = Nsfocus_task.objects.filter(admin_user_id=request.user.id)
    return render_to_response('task/nsfcous_list.html', locals())

def  task_info(request):
    return  render_to_response('task/task.info.html', locals())


