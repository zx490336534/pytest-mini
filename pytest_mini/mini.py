#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2022/11/22 17:23
# @File     : mini.py
# @Desc     : 小程序操作
import json

import allure
import minium
from minium import MiniConfig, MiniAppError, MiniElementNotFoundError
from minium.framework.minitest import init_miniprogram, reset_minium, full_reset

from .constant import Constant
from .locator import Locator
from .logoperator import LogOperator
from .timeoperator import timeoperator

logger = LogOperator(__name__)


class Mini:
    native = None
    appId = ""
    appName = ""
    _app = None
    driver = None
    config = {}
    g_network_message_dict = {}  # 记录请求消息
    g_network_req_cache = {}  # 记录请求体消息(降低重复请求消息量)
    g_network_resp_cache = {}  # 记录请求返回消息(降低重复请求消息量)
    g_log_message_list = []
    last_request = {}

    def __init__(self, driver=None):
        # 基础配置
        self.base_config = {
            "project_path": Constant.PROJECT_PATH,
            "dev_tool_path": Constant.DEV_TOOL_PATH,
            "auto_authorize": True,
            "outputs": Constant().LOG_PATH,
        }
        self.page_name = ""
        if driver:
            self.native, self.mini = driver

    def open(self, config: dict = None):
        if config is None:
            config = {}
        self.config = {**self.base_config, **config}
        logger.info(f"使用「{self.config}」启动小程序")
        self.native, self.mini, miniprogram = init_miniprogram(MiniConfig(self.config))
        self.driver = self.native, self.mini
        self.enable_app_log()
        self.enable_network_panel()

    def enable_app_log(self):
        self.app.connection.register("App.logAdded", self.save_log)
        self.app.connection.send("App.enableLog")

    def save_log(self, message):
        message["dt"] = timeoperator.now1
        self.g_log_message_list.append(message)

    def enable_network_panel(self):
        self.app._evaluate_js("uuid")
        self.app.expose_function("mini_request_callback", self.request_callback)
        self.app.expose_function("mini_send_request", self.send_request)
        self.app._evaluate_js("networkPannel")

    def request_callback(self, message):
        [msg_id, res, ms, hash_id] = message["args"]
        if hash_id and res:  # 传了原始response res, 记录起来
            self.g_network_resp_cache[hash_id] = {"res": res, "timestamp": timeoperator.now1}
        elif hash_id and hash_id in self.g_network_resp_cache:
            res = self.g_network_resp_cache[hash_id]["res"]
            self.g_network_resp_cache[hash_id]["timestamp"] = timeoperator.now1
        if msg_id not in self.g_network_message_dict:
            self.g_network_message_dict[msg_id] = {"timestamp": timeoperator.now1}
        self.g_network_message_dict[msg_id]["end_timestamp"] = ms
        self.g_network_message_dict[msg_id]["response"] = json.loads(res)
        self.last_request["response"] = self.g_network_message_dict[msg_id]

    def send_request(self, message):
        [msg_id, obj, ms, hash_id] = message["args"]
        if hash_id and obj:  # 传了原始request obj, 记录起来
            self.g_network_req_cache[hash_id] = {"obj": obj, "timestamp": timeoperator.now1}
        elif hash_id and hash_id in self.g_network_req_cache:
            obj = self.g_network_req_cache[hash_id]["obj"]
            self.g_network_req_cache[hash_id]["timestamp"] = timeoperator.now1
        if msg_id not in self.g_network_message_dict:
            self.g_network_message_dict[msg_id] = {"timestamp": timeoperator.now1}
        self.g_network_message_dict[msg_id]["start_timestamp"] = ms
        self.g_network_message_dict[msg_id]["request"] = json.loads(obj)
        self.last_request["request"] = self.g_network_message_dict[msg_id]

    @property
    def app(self) -> minium.App:
        if not self.mini:
            raise MiniAppError("未启动小程序")
        return self._app or (self.mini and self.mini.app)

    @app.setter
    def app(self, value):
        self._app = value

    @property
    def page(self) -> minium.Page:
        if not self.mini:
            raise MiniAppError("未启动小程序")
        return self.mini.app.get_current_page()

    @allure.step("截图并存放到「{path}」中")
    def screenshot_pic(self, path: str):
        self.native.screen_shot(path)

    @allure.step("关闭小程序")
    def close(self):
        reset_minium()

    @allure.step("退出小程序")
    def quit(self):
        full_reset()

    def find_element(self, locator: Locator):
        wait_sec = locator.wait_sec
        element = locator.element
        inner_text = locator.inner_text
        value = locator.value
        text_contains = locator.text_contains
        desc = self.page_name + locator.desc

        try:
            el = self.page.get_element(
                selector=element,
                inner_text=inner_text,
                text_contains=text_contains,
                value=value,
                max_timeout=wait_sec
            )
        except Exception as e:
            raise MiniElementNotFoundError(f"没有找到{desc}:{e}")
        return el

    def find_elements(self, locator: Locator):
        wait_sec = locator.wait_sec
        element = locator.element
        inner_text = locator.inner_text
        value = locator.value
        text_contains = locator.text_contains
        desc = self.page_name + locator.desc

        try:
            el = self.page.get_elements(
                selector=element,
                inner_text=inner_text,
                text_contains=text_contains,
                value=value,
                max_timeout=wait_sec
            )
        except Exception as e:
            raise MiniElementNotFoundError(f"没有找到{desc}:{e}")
        return el

    @allure.step("点击「{locator}」")
    def click(self, locator: Locator, many: bool = False, num: int = 0):
        """
        点击元素
        :param locator:
        :param many: 是否会定位到多个
        :param num: 定位到多个后选择其中某一个
        :return:
        """
        if many:
            ele = self.find_elements(locator)[num]
        else:
            ele = self.find_element(locator)
        ele.click()

    @allure.step("往「{locator}」中输入「{text}」")
    def input(self, locator: Locator, text='', many: bool = False, num: int = 0):
        """
        往元素中输入内容
        :param locator:
        :param text:
        :param many: 是否会定位到多个
        :param num: 定位到多个后选择其中某一个
        :return:
        """
        if many:
            ele = self.find_elements(locator)[num]
        else:
            ele = self.find_element(locator)
        ele.input(text)

    @allure.step("按住「{locator}」往({x_offset}, {y_offset})方向移动")
    def move(self, locator: Locator, x_offset, y_offset, move_delay=350, smooth=False, many: bool = False,
             num: int = 0):
        """
        移动元素
        :param locator:
        :param x_offset: x 方向上的偏移，往右为正数，往左为负数
        :param y_offset: y 方向上的偏移，往下为正数，往上为负数
        :param move_delay: 移动延时 (ms)
        :param smooth: 是否平滑移动
        :param many: 是否会定位到多个
        :param num: 定位到多个后选择其中某一个
        :return:
        """
        if many:
            ele = self.find_elements(locator)[num]
        else:
            ele = self.find_element(locator)
        ele.move(x_offset, y_offset, move_delay, smooth)

    @allure.step("清除用户授权信息(公共库 2.9.4 开始生效)")
    def clear_auth(self):
        try:
            self.mini.clear_auth()
        except Exception as e:
            logger.error(f"清除用户授权信息失败:{e}")

    @allure.step("获取系统信息")
    @property
    def system_info(self):
        return self.mini.get_system_info()

    @allure.step("注入代码并执行")
    def evaluate(self, function: str, args, sync=False):
        """
        向 app Service 层注入代码并执行
        :param function:代码字符串
        :param args:参数
        :param sync:是否同步执行
        :return:
        :except:
            同步
            * result = evaluate("function(){args=arguments;return 'test evaluate: '.concat(Array.from(args));}", args, sync=True)
            异步
            * msg_id = self.app.evaluate("function(){args=arguments;return 'test evaluate: '.concat(Array.from(args));}", args, sync=False)
                * result = self.app.get_async_response(msg_id, 5)
        )
        """
        self.app.evaluate(function, args, sync)

    @allure.step("mock 接口请求")
    def mock_request(self, rule: str or dict, success=None, fail=None):
        """

        :param rule: 规则
        :param success: 成功返回的数据
        :param fail: 失败返回的数据
        with mock_request(rule={"url": ".*/SendMsg.*"}, success={"data": "mock result3", "statusCode": 200}):
            ...
        """
        return MockRequest(self.app, rule=rule, success=success, fail=fail)

    @allure.step("回到首页")
    def home(self):
        self.app.go_home()

    @allure.step("回到上一页")
    def back(self):
        self.app.navigate_back()

    @allure.step("跳转到「{path}」页面")
    def go_to(self, path):
        self.app.relaunch(path)

    @allure.step("等待页面跳转成功")
    def wait_page(self, path, max_timeout=10):
        self.app.wait_for_page(path, max_timeout)

    @allure.step("滚动到「(x)」位置")
    def scroll_to(self, x):
        self.page.scroll_to(x)

    @allure.step("查看「{locator}」是否存在")
    def has_element(self, locator):
        ret = False
        try:
            ele = self.find_element(locator)
            if ele:
                ret = True
        except Exception as e:
            logger.error(f"查看元素「{locator}」是否存在异常:{e}")
        return ret

    @allure.step("处理对话框")
    def confirm_dialog(self, flag=True, method="showModal", result=None):
        """

        :param flag: True=确认,False=取消
        :param method:
        :param result: 传入result时,flag不起作用
        :return:
        """
        if result is None:
            return MockWxMethod(self.app, method=method, result={"confirm": flag})
        else:
            return MockWxMethod(self.app, method=method, result=result)

    def mock_make_phone_call(self, result=None):
        if result is None:
            result = {"confirm": False}
        return MockWxMethod(self.app, method="makePhoneCall",
                            functionDeclaration="""function(options){console.log(options)}""", result=result)


class MockWxMethod:
    """
    https://minitest.weixin.qq.com/#/minium/Python/api/App?id=mock_wx_method
    """

    def __init__(self, app, **kwargs):
        self.app = app
        self.kwargs = kwargs
        self.method = self.kwargs.get("method")

    def __enter__(self):
        logger.info(f"开启{self.method}的mock")
        self.app.mock_wx_method(**self.kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"关闭{self.method}的mock")
        self.app.restore_wx_method(self.method)


class MockRequest:
    def __init__(self, app, **kwargs):
        self.app = app
        self.kwargs = kwargs

    def __enter__(self):
        self.app.mock_request(**self.kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.restore_request()


if __name__ == '__main__':
    mini = Mini()
    print(mini.page)
