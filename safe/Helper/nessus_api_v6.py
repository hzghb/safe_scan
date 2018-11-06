#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/21 下午4:08
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : nessus_api_6.py.py
# @Software: PyCharm
import sys
# sys.path.append("..")

import requests, json, csv, os, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# from core.settings import talscan_config,redis_task
from host_type_check import *

talscan_config = {"report_filters": {
    "awvs_white_list": ["orange", "red", "blue"],  # green,blue,orange,red四种级别
    "nessus_white_list": ["High", "Medium", "Low"],
    "bug_black_list": [  # 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
        "User credentials are sent in clear text"
    ]
}
}


class Work(object):
    def __init__(self, scan_id="", scan_uuid="",scan_target="", scan_type="", scan_args="", back_fn=None):
        self.api_url = 'https://192.168.29.198:8834'
        self.username = "root"
        self.password = "xxxxxxxx"
        self.filter = talscan_config["report_filters"]
        self.report_save_dir = '/tmp/'
        self.verify = False
        self.token = ''
        self.enable = True
        self.scan_uuid=scan_uuid
        self.scan_id = scan_id
        self.target = scan_target
        self.scan_type = scan_type
        self.args = scan_args
        self.back_fn = back_fn
        self.result = {}

    def connect(self, method, resource, data=None, params=None):
        headers = {'X-Cookie': 'token={0}'.format(self.token), 'content-type': 'application/json'}
        data = json.dumps(data)

        try:
            if method == 'POST':
                r = requests.post(str(self.api_url + resource), data=data, headers=headers, verify=self.verify)

            elif method == 'PUT':
                r = requests.put(str(self.api_url + resource), data=data, headers=headers, verify=self.verify)
            elif method == 'DELETE':
                r = requests.delete(str(self.api_url + resource), data=data, headers=headers, verify=self.verify)
            else:
                r = requests.get(str(self.api_url + resource), params=params, headers=headers, verify=self.verify)
        except Exception, e:
            print  e
            return {"status": 3}

        if r.status_code == 200:
            try:
                data = r.json()
            except:
                data = r.content

            result = {"status": 1, "data": data}
            return result
        else:
            result = {"status": 3}
            return result

    def nessus_login(self):
        login = {'username': self.username, 'password': self.password}
        data = self.connect('POST', '/session', data=login)
        print data
        status = data["status"]
        print status
        if status == 1:
            result = {"status": 1, "data": data["data"]['token']}
            print  result
            return result
        else:
            result = {"status": 0}
            print result
            return result

    def nessus_process_status(self, sid):
        # canceled,running,completed
        data = self.nessus_login()
        status = data["status"]
        if status == 1:
            token = data["data"]
        else:
            result = {"status": 0}
            return result

        headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
        url = self.api_url + '/scans/'
        data = requests.get(url=url, params=None, headers=headers, verify=self.verify)
        res = data.json()
        info1=res['scans']
        print info1
        try:
            return  info1
        except:
            return {"status": 0}
    def  nessus_policies(self,):
        data = self.nessus_login()
        status = data["status"]
        if status == 1:
            token = data["data"]
        else:
            result = {"status": 0}
            return result

        headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
        url = self.api_url + '/policies/'
        data = requests.get(url=url, params=None, headers=headers, verify=self.verify)
        res = data.json()
        info=res['policies']
        print info
        try:
            return info
        except:
            return {"status": 0}


    def nessus_add_task(self):
        if is_domain(self.target) or is_host(self.target):
            create_data = {
                "uuid": self.scan_uuid,
                # "uuid": 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',#选择策略
                "settings": {
                    "name": self.scan_id,
                    "scanner_id": "1",
                    "text_targets": self.target,
                    "enabled": False,
                    "launch_now": True,
                }
            }
            post_data = json.dumps(create_data)

            data = self.nessus_login()
            status = data["status"]
            if status == 1:
                token = data["data"]
            else:
                print  '99'
                return {"status": 2, "data": "NESSUS >>>> :登陆失败"}

            headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
            r = requests.post(url=str(self.api_url + '/scans'), data=post_data, headers=headers, verify=self.verify)

            if r.status_code == 200:
                try:
                    get_id = r.json()
                except:
                    get_id = r.content

                sid = get_id['scan']['id']
                result = {"status": 1, "data": sid}
                return result
            else:
                result = {"status": 2, "data": "NESSUS >>>> :增加任务失败"}
                return result
        else:
            return {"status": 2, "data": "NESSUS >>>> :格式错误"}

    def nessus_stop_task(self, sid):
        data = self.nessus_login()
        status = data["status"]
        if status == 1:
            token = data["data"]
        else:
            result = {"status": 0}
            return result

        headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
        url = str(self.api_url + '/scans/{0}/stop/'.format(sid))
        r = requests.post(url=url, params=None, headers=headers, verify=self.verify)
        if r.status_code == 200:
            result = {"status": 1}
            return result
        else:
            result = {"status": 0}
            return result

    def nessus_report_task(self, taskid, sid):
        bug_list = []

        data = self.nessus_login()
        status = data["status"]
        if status == 1:
            token = data["data"]
        else:
            result = {"status": 0}
            return result

        headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
        url = str(self.api_url + '/scans/{0}/export'.format(sid))
        data = json.dumps({"format": "csv"})
        r = requests.post(url=url, data=data, headers=headers, verify=self.verify)
        try:
            file = r.json()['token']
        except:
            result = {"status": 0}
            return result
        down_file_url = str(self.api_url + '/scans/exports/{0}/download'.format(file))
        r = requests.get(url=down_file_url, headers=headers, verify=self.verify)

        csv_file = str(self.report_save_dir + "{0}_nessus.csv".format(str(taskid)))
        f = open(csv_file, 'wb')
        data = r.content
        f.write(data)
        f.close()

        csv_open_file = open(csv_file, 'rb')
        csvReader = csv.reader(csv_open_file)
        for row in csvReader:
            parameterStr = ','.join(row)
            parameters = parameterStr.split(',')
            PID = parameters[0]
            CVE = parameters[1]
            CVSS = parameters[2]
            Risk = parameters[3]
            Host = parameters[4]
            Protocol = parameters[5]
            Port = parameters[6]
            Name = parameters[7]
            Synopsis = parameters[8]
            Description = parameters[9]
            Solution = parameters[10]
            See_Also = parameters[11]
            Plugin_Output = parameters[12]

            bug_name = str(Name)
            bug_level = str(Risk)
            bug_summary = str(Synopsis) + "\r\n" + str(Description)
            bug_detail = "Bug Port : " + str(Port) + "\r\n" + "CVE : " + str(CVE)
            bug_repair = str(Solution) + "\r\n" + str(Plugin_Output)

            if str(Risk) in self.filter['nessus_white_list']:
                bug_list.append(
                    {'bug_name': bug_name, 'bug_level': bug_level, 'bug_summary': bug_summary, 'bug_detail': bug_detail,
                     'bug_repair': bug_repair})

        csv_open_file.close()
        # os.remove(csv_file)

        if len(bug_list) > 0:
            result = {"status": 1, "data": bug_list}
            return bug_list
        else:
            result = {"status": 0}
            return result

    def run(self):
        result = self.nessus_add_task()
        status = result["status"]

        if status == 1:
            nessus_id = int(result["data"])
            while True:
                time.sleep(5)
                nessus_process = self.nessus_process_status(nessus_id)
                nessus_status = nessus_process["status"]
                if nessus_status == 1:
                    nessus_process_data = nessus_process["data"].encode("utf8")
                    if nessus_process_data == "completed":
                        break

            time.sleep(20)  # 推迟20秒，获取报告;nessus任务进程到100有部分延迟结束时间
            nessus_report = self.nessus_report_task(self.scan_id, nessus_id)
            nessus_report_status = nessus_report["status"]
            if nessus_report_status == 1:
                nessus_report_data = nessus_report["data"]
                data = []
                for line in nessus_report_data:
                    task_result = {
                        "scan_id": self.scan_id,
                        "model": "nessus",
                        "bug_author": "bing",
                        "bug_name": line["bug_name"],
                        "bug_level": line["bug_level"],
                        "bug_summary": line["bug_summary"],
                        "bug_detail": line["bug_detail"],
                        "bug_repair": line["bug_repair"]
                    }
                    redis_task.sadd("nessus_result", task_result)
                    print task_result

                # 任务最终结束
                final_result = {"status": 1, "scan_id": self.scan_id, "model": "nessus"}

                redis_task.sadd("nessus_result", final_result)
                print final_result

            else:
                # 任务最终结束
                final_result = {"status": 1, "scan_id": self.scan_id, "model": "nessus"}

                redis_task.sadd("nessus_result", final_result)
                print final_result

        elif status == 2:
            nessus_error = result["data"]
            final_result = {"status": 2, "data": nessus_error, "scan_id": self.scan_id, "model": "nessus"}

            redis_task.sadd("nessus_result", final_result)
            print final_result


#t = Work("1234455","ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66","www.baidu.com")
#s = t.nessus_report_task(5,84)
#print s
