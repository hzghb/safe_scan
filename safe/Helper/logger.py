#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 下午5:04
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : logger.py.py
# @Software: PyCharm


import logging.config
logging.config.fileConfig("/root/web/config/logger.ini")
logger = logging.getLogger("safe")

if __name__=='__main__':
    logger.info(msg="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    logger.error(msg="eyJ1c2VybmFtZSI6IndlbGxpYW0iLCJ1c2VyX2lkIjoyLCJlbWFpbCI6IjMwMzM1MDAxOUBxcS5jb20iLCJleHAiOjE1MTk2NTUzNTB9")