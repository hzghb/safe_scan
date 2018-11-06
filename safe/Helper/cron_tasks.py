#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 下午8:55
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : cron_tasks.py.py
# @Software: PyCharm


import datetime
import json
from djcelery import models as celery_models
from django.utils import timezone


def create_task(name, task, task_args, crontab_time):

    # task任务， created是否定时创建
    task, created = celery_models.PeriodicTask.objects.get_or_create(
        name=name,
        task=task)
    # 获取 crontab
    crontab = celery_models.CrontabSchedule.objects.filter(
        **crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = celery_models.CrontabSchedule.objects.create(
            **crontab_time)
    task.crontab = crontab  # 设置crontab
    task.enabled = True  # 开启task
    task.kwargs = json.dumps(task_args)  # 传入task参数
    expiration = timezone.now() + datetime.timedelta(days=1)
    task.expires = expiration  # 设置任务过期时间为现在时间的一天以后
    task.save()
    return True


def disable_task(name):
    '''
    关闭任务
    '''
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False  # 设置关闭
        task.save()
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return True