#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from safe.Helper import Checkcode
import StringIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from  safe.models import    *
from  safe.Helper  import   log
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


def blog(request):
    return render(request, 'blog.html')
