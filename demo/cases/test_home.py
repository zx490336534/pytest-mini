#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/4 14:51
# @File     : test_home.py
# @Project  : PyCharm
import allure

from pytest_mini import compose


@compose(feature="小程序官方组件展示", story="组件", title='容器视图操作')
def test_view_container(components_page):
    with allure.step("点击容器视图"):
        components_page.click(components_page.view_container)
        assert False, "故意失败,查看报告截图"
