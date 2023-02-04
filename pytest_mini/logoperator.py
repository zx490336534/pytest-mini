#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2021/7/15 15:49
# @File     : logoperator.py
# @Project  : WYTest
# @Desc     : 日志操作
import os
import logging
from logging.handlers import BaseRotatingHandler, TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
from .constant import Constant
from .timeoperator import timeoperator


class LogOperator:
    sh = logging.StreamHandler()

    def __init__(self, name, path=Constant().LOG_PATH, level=None, RotatingFileHandler: BaseRotatingHandler = None,
                 isprint=None):
        log = logging.getLogger(name)
        level = 'DEBUG'
        self.isprint = isprint
        log.setLevel(level)
        self.log = log
        self.name = name
        if path:
            if not os.path.isdir(path):
                os.mkdir(path)
            if RotatingFileHandler and isinstance(RotatingFileHandler, BaseRotatingHandler):
                fh = RotatingFileHandler
            elif RotatingFileHandler and isinstance(RotatingFileHandler, TimedRotatingFileHandler):
                fh = TimedRotatingFileHandler(os.path.join(path, 'logging.log'), when='d',
                                              interval=1, backupCount=7,
                                              encoding="utf-8")
            else:
                fh = ConcurrentRotatingFileHandler(os.path.join(path, 'logging.log'),
                                                   maxBytes=10 * 1024 * 1024,
                                                   backupCount=7, encoding="utf-8")
            fh.setLevel(level)
            self.log.addHandler(fh)
            formatter = logging.Formatter("[%(asctime)s] | 【%(levelname)s】 | <%(name)s> | %(message)s")
            fh.setFormatter(formatter)

    def debug(self, message):
        self.fontColor('\033[0;34m{}\033[0;34m{}\033[0;34m{}\033[0;34m{}')
        self.log.debug(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【DEBUG】 | <{self.name}> | {message}")

    def info(self, message):
        self.fontColor('\033[0;32m{}\033[0;32m{}\033[0;32m{}\033[0;32m{}')
        self.log.info(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【INFO】 | <{self.name}> | {message}")

    def warning(self, message):
        self.fontColor('\033[0;33m{}\033[0;43m{}\033[0;33m{}\033[0;33m{}')
        self.log.warning(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【WARNING】 | <{self.name}> | {message}")

    def error(self, message):
        self.fontColor('\033[0;31m{}\033[0;41m{}\033[0;31m{}\033[0;31m{}')
        self.log.error(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【ERROR】 | <{self.name}> | {message}")

    def exception(self, message):
        self.fontColor('\033[0;31m{}\033[0;41m{}\033[0;31m{}\033[0;31m{}')
        self.log.exception(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【ERROR】 | <{self.name}> | {message}")

    def critical(self, message):
        self.fontColor('\033[0;35m{}\033[0;45m{}\033[0;35m{}\033[0;35m{}')
        self.log.critical(message)
        if self.isprint:
            print(f"[{timeoperator.now1}] | 【CRITICAL】 | <{self.name}> | {message}")

    def fontColor(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color.format("[%(asctime)s] | ",
                                                   "【%(levelname)s】", "| <%(name)s> ", " | %(message)s"))
        self.sh.setFormatter(formatter)
        self.log.addHandler(self.sh)


if __name__ == '__main__':
    logger = LogOperator("logger")
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('CRITICAL')
