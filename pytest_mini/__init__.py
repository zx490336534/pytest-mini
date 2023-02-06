#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/4 10:20
# @File     : __init__.py
# @Project  : PyCharm
__version__ = "0.1.19"
__description__ = "pytest版 微信小程序测试"

from .allureoperator import compose, attach_png, attach_text, request_allure
from .locator import Locator
from .logoperator import LogOperator
from .mini import Mini, MockWxMethod, MockRequest
from .plugin import plugins
from .timeoperator import timeoperator
from .tools import *
