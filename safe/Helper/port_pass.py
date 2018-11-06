#!coding:utf-8
import optparse, re, subprocess, socket, time, os, nmap,time ,uuid,sys
from threading import *
from IPy import IP
from  safe.Helper import SQL_db
from safe.models import  *
import django.utils.timezone as timezone
class Work(object):
    def __init__(self,assets_id,user_id,tgtHost,task_id,tgtPort='1-65535',):
        self.assets_id=assets_id
        self.user_id=user_id
        self.tgtHost=tgtHost
        self.tgtPort=tgtPort
        self.task_id =task_id
        self.connection_lock_1= BoundedSemaphore(value=1000)

    def get_port_list(self,port_list):
        port_list = self.tgtPort.split('-')
        start_num = int(port_list[0]) + 1
        end_num = int(port_list[1])
        for j in range(start_num, end_num):
            port_list.append(str(j))
        return port_list


    def portScan(self,ip, port_list):
            for port in port_list:
                self.connection_lock_1.acquire()
                t = Thread(target=self.connPort, args=(ip, port))
                t.start()

    def connPort(self,ip, port):
        st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st.settimeout(0.2)
        try:
            st.connect((ip, int(port)))
            SQL_db.port_db(assets_id=self.assets_id,ip=ip,port=port,task_id=self.task_id, user_id=self.user_id)
            self.get_server(ip, port)
            st.close()
        except Exception as e:
            pass
        self.connection_lock_1.release()

    def get_server(self,ip, port):
        print ip,port
        port_info=[]
        try:
            r=os.popen('nmap %s  -p %s  -A' %(ip,port))
            re = '%s/tcp' % (port)
            for line in r.readlines():
                if re in line.strip():
                    t = line.strip().split(' ')
                    serviceversion = ''
                    while '' in t:
                        t.remove('')
                    for i in range(len(t)):
                        if i == 2:
                            servicename = t[i]
                        elif i > 2:
                            serviceversion= serviceversion + t[i]
            SQL_db.os_port_db(assets_id=self.assets_id,ip=ip,port=port,task_id=self.task_id, user_id=self.user_id,
                              servicename=servicename,serviceversion=serviceversion
                              )
        except Exception as e:
            print e
            print  '*************************************************8'

    def  run(self):
        Portpass_task.objects.filter(id=self.task_id).update(portpass_status=2)
        try:
         Sub_task.objects.filter(task_scan_id=self.task_id,ip=self.tgtHost).update(start_date=timezone.now())
        except Exception  as  e:
            print e
        print self.tgtHost
        port_list = self.get_port_list(self.tgtPort)
        info=self.portScan(self.tgtHost, port_list)
        return  'ok'
