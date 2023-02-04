#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2022/11/22 17:20
# @File     : constant.py
# @Desc     : 常量
import inspect
import os


def get_env(name, base=''):
    """
    从环境变量中获取指的信息
    @param name: 环境变量信息
    @param base: 默认信息
    @return:
    """
    return os.getenv(name) and os.getenv(name).strip() or base


BASE_PATH = os.path.dirname(inspect.stack()[1].filename)  # 根路径
SRC_PATH = os.path.join(BASE_PATH, 'src')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
TEST_PIC = os.path.join(REPORT_PATH, 'test_pic')
TOOL_PATH = os.path.join(SRC_PATH, 'tools')
ALLURE_TOOL_PATH = os.path.join(TOOL_PATH, 'allure-2.14.0/bin')

# PROJECT_PATH = get_env("project_path", "/Users/zhongxin/gitproject/design-zone-mp/dist")  # 待测试的小程序项目路径
PROJECT_PATH = get_env("project_path", "/Users/zhongxin/gitproject/intelligentdesign/dist")  # 待测试的小程序项目路径
DEV_TOOL_PATH = get_env("dev_tool_path", "/Applications/wechatwebdevtools.app/Contents/MacOS/cli")  # 微信开发者工具路径

for i in [LOG_PATH, REPORT_PATH, TEST_PIC]:
    if not os.path.exists(i):
        os.mkdir(i)


class USERINFO:
    username = "onlinedingzhi@fengfei.com"
    password = "123456"
    # sit
    # nickname = '客户端005'
    # phone = "18817244832"
    # beta
    nickname = 'onlinedingzhi'
    phone = "18411632866"


if __name__ == '__main__':
    print(BASE_PATH)
