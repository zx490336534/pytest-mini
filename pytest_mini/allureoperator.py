#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2021/7/20 10:11
# @File     : allureoperator.py
# @Project  : WYTest
# @Desc     : allure相关操作
# 官网地址:https://docs.qameta.io/allure/
import time
import builtins
import allure

from .logoperator import LogOperator
from .timeoperator import timeoperator

logger = LogOperator(__name__)


def compose(**kwargs):
    """
    将头部ALlure装饰器进行封装
    可以采用：
        feature='模块名称'
        story='用户故事'
        title='用例标题'
        testcase='测试用例链接地址'
        severity='用例等级(blocker、critical、normal、minor、trivial)'
        link='链接'
        testcase=("url", "xx测试用例")
        issue=('bug地址', 'bug名称')
    的方式入参数
    :param kwargs:
    :return:
    """

    def deco(f):
        builtins.__dict__.update({'allure': allure})
        _kwargs = [('allure.' + key, value) for key, value in kwargs.items()]
        for allurefunc, param in reversed(_kwargs):
            if param:
                if isinstance(param, tuple):
                    f = eval(allurefunc)(*param)(f)
                else:
                    f = eval(allurefunc)(param)(f)
            else:
                f = eval(allurefunc)(f)
        return f

    return deco


def request_allure(req):
    """
    接口操作报告展示装饰器
    """

    def send(*args, **kwargs):
        start = time.process_time()
        response = req(*args, **kwargs)
        end = time.process_time()
        usetime = f'{end - start:.3f}秒'
        attach_text(f'以「{response.request.method}」方式请求「{response.url}」;'
                    f'返回状态码为「{response.status_code}」'
                    f'耗时「{usetime}」'
                    f'返回内容为「{response.text}」',
                    "接口请求")
        attach_text(timeoperator.now1, "请求时间")
        attach_text(response.url, "url")
        attach_text(response.request.method, "请求方式")
        attach_text(response.status_code, "状态码")
        attach_text(response.text, "返回内容-text")
        attach_text(response.json(), "返回内容-json")
        attach_text(usetime, "耗时")
        return response

    return send


def attach_png(pic_path, name, ele=None):
    """
    将png图片存放到allure报告上
    :param pic_path: 图片位置
    :param name: 展示的名称
    :param ele: driver对象
    :return:
    """
    try:
        if ele:
            ele.screenshot_pic(pic_path)
        allure.attach.file(source=pic_path, name=name, attachment_type=allure.attachment_type.PNG)
        logger.info(f'截图 {name}，存放到 {pic_path} 成功！')
    except Exception as e:
        logger.error(f'存放图片{name}失败:{e}')


def attach_text(body, name):
    """
    将text放在allure报告上
    :param body: 内容
    :param name: 标题
    :return:
    """
    try:
        allure.attach(body=str(body), name=str(name), attachment_type=allure.attachment_type.TEXT)
        logger.info(f'存放文字 {name}:{body} 成功！')
    except Exception as e:
        logger.error(f'存放文字失败 {name}:{body}！:{e}')
