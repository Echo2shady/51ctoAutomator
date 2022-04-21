#!usr/bin/env python
# -*- coding:utf-8 -*-
# user nanme: Mr.zhang
# data time : 2022/1/6   2:08 下午
# project   : loggers.py
# IDE       : PyCharm
# email     :17600960626@163.com
import os
import logging
import logging.handlers
import time

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# @singleton
class JFMlogging(object):
    def __init__(self):
        # host_name = socket.gethostname()
        # ip = socket.gethostbyname(host_name)
        log_path = 'logs'  # 日志存放目录
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = os.path.join(log_path, "{}.log".format(time.strftime("%Y%m%d")))

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.logging_msg_format = '[%(asctime)s] [%(levelname)s] [%(module)s.py-line:%(lineno)d] %(message)s'
        self.formater = logging.Formatter(self.logging_msg_format)

        self.fileHandler = logging.FileHandler(log_file, mode='a', encoding="UTF-8")
        self.fileHandler.setFormatter(self.formater)
        self.fileHandler.setLevel(logging.INFO)

        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.console.setFormatter(self.formater)

        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.console)

    # def getloger(self):
    #     return self.logger


log = JFMlogging().logger