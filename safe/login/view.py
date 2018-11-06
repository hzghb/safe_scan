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

def CheckCode(request):
    mstream = StringIO.StringIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")

    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]

    return HttpResponse(mstream.getvalue())





@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        check_code = request.POST.get('code')

        session_code = request.session["CheckCode"]
        if check_code.strip().lower() != session_code.lower():
            return HttpResponse('400')
        else:
            userinfo = auth.authenticate(username=username, password=password)
            if userinfo:
                if userinfo.is_active:
                    auth.login(request, userinfo)
                    meta = request.META
                    # group_id= Group.objects.get(id=request.user.id)
                    # print  group_id
                    log.login(meta['REMOTE_ADDR'],meta['HTTP_USER_AGENT'],request.user.id,0)
                    return HttpResponse('200')
            else:
                return HttpResponse('400')

    else:
       return render_to_response('login.html')

@login_required
def logout(request):
    meta = request.META
    log.logout(meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT'], request.user.id,0)
    auth.logout(request)
    return render(request, 'login.html')



def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')






