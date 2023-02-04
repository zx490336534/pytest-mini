#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/4 00:06
# @File     : fixture.py
# @Project  : PyCharm
import os
import time
import inspect
from typing import Union

import allure
import allure_commons
import pytest
from allure_commons.model2 import TestResult, TestResultContainer

from .allureoperator import attach_png
from .constant import TEST_PIC
from .logoperator import LogOperator
from .mini import Mini

logger = LogOperator(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 失败后执行
    :param item: 测试用例
    :param call: 测试步骤
    :return:
    """
    out = yield
    result = out.get_result()
    logger.info(f"测试报告:{result}")
    logger.info(f"执行耗时:{call.duration}")
    if result.outcome in ['failed', 'error']:
        for k, v in item.funcargs.items():
            try:
                if hasattr(v, 'native'):
                    attach_png(f'{TEST_PIC}/{int(time.time())}.png', "失败截图", v)
                    break
            except Exception as e:
                logger.error(f"失败截图异常:{e}")


def pytest_assume_fail(lineno, entry):
    """
    assume 断言报错截图
    """
    print(entry)
    for i in inspect.stack():
        if os.path.split(i.filename)[1].startswith('test_'):
            try:
                for k, v in i.frame.f_locals.items():
                    if hasattr(v, 'native'):
                        attach_png(f'{TEST_PIC}/{int(time.time())}.png', f"失败截图_{int(time.time())}", v)
                        break
            except Exception as e:
                logger.error(f"失败截图异常:{e}")


def pytest_collection_modifyitems(session, items):
    """
    修改用例执行顺序
    :param session: 会话信息
    :param items: 用例列表
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
    logger.info(f"收集到的测试用例:{items}")


@pytest.fixture(autouse=True)
def case_end():
    """
    描述中增加用例执行步骤
    """
    yield
    description = []

    def get_steps(data, steps_data, num: Union[str, int] = 1):
        name = getattr(data, 'name')
        steps = getattr(data, 'steps')
        if "." in num and '」' in num:
            num = num.split("」")[1]
        if steps:
            steps_data.append(f'{num}:{name}')
            n = 0
            for j in steps:
                n += 1
                get_steps(j, steps_data, f"{num}.{n}")
        else:
            steps_data.append(f'{num}:{name}')

    for k, v in allure_commons.reporter.ThreadContextItems._thread_context.items():
        num = 1
        for k1, v1 in v.items():
            steps_data = []
            befores = hasattr(v1, 'befores') and getattr(v1, 'befores') or []
            steps = hasattr(v1, 'steps') and getattr(v1, 'steps') or []
            if isinstance(v1, TestResultContainer):
                for i in befores:
                    get_steps(i, steps_data, f"「前置」{num}")
            if isinstance(v1, TestResult):
                for i in steps:
                    get_steps(i, steps_data, f"「case」{num}")
            if steps_data and all(
                    [
                        "_session_faker" not in steps_data[0],
                        "case_end" not in steps_data[0],
                    ]):
                description.append(steps_data)
                num += 1

    description_text = ""
    for i in description:
        for j in i:
            num1 = j.split(":")[0].count(".") * 2
            if num1 > 0:
                description_text += f"<p style='text-indent:{num1}em;'>{j}</p>"
            else:
                description_text += f"<p>{j}</p>"
    description_text = f'<div style="line-height: 16px;font-size: 16px">{description_text}</div>'
    logger.info(description_text)
    allure.dynamic.description(description_text)


@pytest.fixture(scope='session')
def mini():
    with allure.step("初始化小程序"):
        mini = Mini()
        mini.open()
    yield mini
    mini.quit()
