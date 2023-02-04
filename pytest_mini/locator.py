#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2022/11/23 10:44
# @File     : locator.py
# @Desc     :

class Locator:
    """
    页面元素封装
    """

    def __init__(self, element, wait_sec=5, desc='', inner_text=None, text_contains=None, value=None):
        """

        @param element: 定位语句
        @param wait_sec: 等待时间 默认5秒
        @param desc: 描述
        @param inner_text: inner_text
        @param value: value
        @param text_contains: 包含的文字
        """
        self.element = element
        self.wait_sec = wait_sec
        self.inner_text = inner_text
        self.text_contains = text_contains
        self.value = value
        self.desc = desc

    def __str__(self):
        inner_text = self.inner_text and f",inner_text:{self.inner_text}" or ""
        text_contains = self.text_contains and f",text_contains:{self.text_contains}" or ""
        value = self.value and f",value:{self.value}" or ""

        return f'{self.desc}:(element:{self.element}[{inner_text}{text_contains}{value}])'

    def __repr__(self):
        return f'{self.desc}'
