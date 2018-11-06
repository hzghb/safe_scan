"""safe_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from  safe.login.view  import   *
from  safe.view import   *
from safe.Assets.views import  *
from safe.scan_task  import   *
from safe.scan_task  import   nsfocus ,pass_port,brute_scan
from safe.blog import  view
from safe.url import  *
from django.conf import settings
from django.conf.urls.static import static
handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    url(r'^api/', include('safe.url.api_url')),
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^test/$',test),
    url(r'^tools/$',tools),
    url(r'^weclome',weclome),
    url(r'^login',login),
    url(r'logout',logout),
    url(r'^checkcode/',CheckCode),
    url(r'^logx',logx),
    url(r'^assets_upload',asset_upload),
    url(r'^assets/$',assets),
    url(r'^add_assets/$',add_assets),
    url(r'^del_assets/$',del_assets),
    url(r'^host_info/(?P<id>[0-9]+)/',host_info),
    url(r'^nsfocus_list',nsfocus.task_list),
    url(r'^task_list',pass_port.task_list),
    url(r'^brute_task',brute_scan.brute_list),
    url(r'^sub_port_task/(?P<id>[0-9]+)/$',pass_port.sub_port_task),
    url(r'^sub_brute_task/(?P<id>[0-9]+)/$',brute_scan.sub_brute_task),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)