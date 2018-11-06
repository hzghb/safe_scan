#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 下午4:28
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : run.py.py
# @Software: PyCharm
import pycurl
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests.packages.urllib3.util.ssl_
import json
import requests
import time
import MySQLdb
import time
import StringIO
import urllib
import json
import xml.dom.minidom

class Work(object):
    def __init__(self,url,username,password):
        self.name=url
        self.username=username
        self.password=password

    def create_xml(self,targets,taskname,port_strategy_userports='1-65535',port_speed='3',scan_level='3',live='yes'):
        #在内存中创建一个空的文档
        doc = xml.dom.minidom.Document()
        # 创建一个根节点Managers对象
        root = doc.createElement('config')
        # 将根节点添加到文档对象中
        doc.appendChild(root)

        managerList = ['server','targets','report','pwdguess','taskname','plugin_template_id','scanpri']
        node_server={
                        'task_type':'ip',
                        'targets':targets,
                        'is_vhost':'yes',
                        'os_match':'no',
                        'messtypes':'5;6;7;8;9;10;11;12;13;14;15;16;17;18;20;21;22;23;24;25;26;27;28',
                        'isguesspwd':'no',
                        'port_strategy':'user',
                        'port_strategy_userports':port_strategy_userports,
                        'port_speed':port_speed,
                        'port_tcp':'T',
                        'port_udp':'no',
                        'live':live,
                        'live_icmp':'yes',
                        'live_udp':'yes',
                        'live_tcp':'yes',
                        'live_tcp_ports':'21,22,23,25,80,443,445,139,3389,6000',
                        'scan_level':scan_level,
                        'timeout_plugins':'40',
                        'timeout_read':'5',
                        'enable_unsafe_plugins':'no',
                        'scan_alert':'yes','alert_msg':'sanca',
                        'scan_huawei':'no',
                        'check_addtional':'no',
                        'scan_oracle':'yes',
                        'ifdebug':'no',
                        'encoding':'UTF-8'

                     }

        for i in managerList:
            print i
            if i == 'server':
             nodeManager = doc.createElement(i)
             root.appendChild(nodeManager)
             for  key, value in node_server.items():
              nodeName = doc.createElement('key')
              nodeName.setAttribute('name',key)
              nodeName.setAttribute('value', value)
              nodeManager.appendChild(nodeName)
            elif i == 'taskname':
                nodeManager = doc.createElement(i)
                nodeManager.appendChild(doc.createTextNode(taskname))
                root.appendChild(nodeManager)
            elif  i == 'plugin_template_id':
                nodeManager = doc.createElement(i)
                nodeManager.appendChild(doc.createTextNode('0'))
                root.appendChild(nodeManager)
            elif  i == 'scanpri':
                nodeManager = doc.createElement(i)
                nodeManager.appendChild(doc.createTextNode('2'))
                root.appendChild(nodeManager)
            else:
                nodeManager = doc.createElement(i)
                root.appendChild(nodeManager)


        # 开始写xml文档
        fp = open('config.xml', 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

    def  addtask(self):
        task_type = '1'
        url = self.name + '/api/task/create?username=' + self.username + '&password=' + self.password+ '&format=json'
        io = StringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, io.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.HTTPPOST, [('config_xml', (curl.FORM_FILE, 'config.xml')),
                                      ('type', (curl.FORM_CONTENTS, task_type)),
                                      ])
        curl.perform()
        ret = io.getvalue()
        io.close()
        curl.close()
        return  ret

    def  task__status(self,task_id):
        url = self.name + 'api/task/status/'+task_id+'?username=' + self.username + '&password=' + self.password + '&format=json'
        response = requests.get(url, verify=False,)
        result = json.loads(response.content)['data']
        print result
        return   result

    def  task__stop(self,task_id):
        url = self.name + 'api/task/stop/'+task_id+'?username=' + self.username + '&password=' + self.password + '&format=json'
        response = requests.post(url, verify=False,)
        result = json.loads(response.content)
        return  result

    def  task__resume(self,task_id):
        url = self.name + 'api/task/resume/'+task_id+'?username=' + self.username + '&password=' + self.password + '&format=json'
        reponse = requests.post(url, verify=False,)
        print  reponse.content

    def  task__delete(self,task_id):
        url = self.name + 'api/task/delete/'+task_id+'?username=' + self.username + '&password=' + self.password + '&format=json'
        reponse = requests.post(url, verify=False,)
        print  reponse.content

    def  task__list(self):
        url = self.name + 'api/task/list?username=' + self.username + '&password=' + self.password + '&format=json'
        print url
        reponse = requests.get(url, verify=False,)
        print  reponse.content

    def task__result(self, task_id):
        url = self.name + 'api/report/task/' + task_id + '?username=' + self.username + '&password=' + self.password + '&format=json'
        print url
        response = requests.get(url, verify=False, )
        info = json.loads(response.content)
        result = info['data']['report']['targets']
        print result
        return result

    def  sys__status(self):
        url = self.name + 'api/system/status?username=' + self.username + '&password=' + self.password + '&format=json'
        print url
        response = requests.get(url, verify=False,)
        result = json.loads(response.content)
        result=result['data']
        print result
        return result
