#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tingbai
# @Time     : 2023/2/4 14:53
# @File     : components_page.py
# @Project  : PyCharm
from pytest_mini import Mini, Locator


class ComponentsPage(Mini):
    view_container = Locator('view', inner_text='视图容器', desc='组件页-视图容器')
