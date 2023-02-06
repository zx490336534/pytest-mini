#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2022/11/22 17:20
# @File     : constant.py
# @Desc     : 常量
import os


def get_env(name, base=''):
    """
    从环境变量中获取指的信息
    @param name: 环境变量信息
    @param base: 默认信息
    @return:
    """
    return os.getenv(name) and os.getenv(name).strip() or base


class Constant:
    BASE_PATH = ""
    PROJECT_PATH = ""  # 待测试的小程序项目路径
    DEV_TOOL_PATH = ""  # 微信开发者工具路径
    CONFIG = None  # 小程序启动配置
    ALLURE_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools/allure-2.14.0/bin/allure')

    @property
    def SRC_PATH(self):
        return os.path.join(Constant.BASE_PATH, 'src')

    @property
    def LOG_PATH(self):
        return os.path.join(Constant.BASE_PATH, 'log')

    @property
    def REPORT_PATH(self):
        return os.path.join(Constant.BASE_PATH, 'report')

    @property
    def TEST_PIC(self):
        return os.path.join(self.REPORT_PATH, 'test_pic')

    @property
    def TOOL_PATH(self):
        return os.path.join(self.SRC_PATH, 'test_pic')

    def __init__(self):
        if Constant.BASE_PATH:
            for i in [self.LOG_PATH, self.REPORT_PATH, self.TEST_PIC]:
                if not os.path.exists(i):
                    os.mkdir(i)
