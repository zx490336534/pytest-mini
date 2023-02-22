#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/4 14:30
# @File     : conftest.py
# @Project  : PyCharm
import pytest

from pytest_mini import plugins
from demo.pages import ComponentsPage

pytest_plugins = plugins(
    "/Users/zhongxin/github/miniprogram-demo",  # 待测试的小程序项目路径
    "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"  # 微信开发者工具路径
)


@pytest.fixture(scope="session")
def components_page(mini):
    yield ComponentsPage(driver=mini.driver)
