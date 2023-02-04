#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/3 23:49
# @File     : plugin.py
# @Project  : PyCharm
import inspect
import os

from .constant import Constant


class Plugin:
    pass


def plugins(project_path="", dev_tool_path="", config=None):
    Constant.BASE_PATH = os.path.dirname(inspect.stack()[1].filename)
    Constant.PROJECT_PATH = project_path
    Constant.DEV_TOOL_PATH = dev_tool_path
    Constant.CONFIG = config
    constant = Constant()
    return ["pytest_mini.fixture"]
