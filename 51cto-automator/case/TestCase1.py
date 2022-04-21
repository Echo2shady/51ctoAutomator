import re
import time
import os
from lib.loggers import log
import allure
import pytest
from selenium.webdriver.common.by import By

import golVar
from lib.device_data import get_vm_size
from lib.get_path import get_path_data
from page.home_page import HomePage
from page.login_page import LoginPage

from public.base_function import PATH

'''
生成allure报告 2 步：
1、python3 -m pytest testcase/TestCase1.py --alluredir report/allure_raw --clean-alluredir
2、allure generate report/allure_raw -o report/html --clean
'''

screen_size_list = []
test_case_data = get_path_data('/data/case_data.yml')
test_adb_data = get_path_data('/data/adb_data.yml')


@allure.story('首页')
# 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
def test_Func_01_01_0002(set_device_id_list, set_driver_pool, cmdopt):
    # pool 池中 driver 与 device_id 为一对一的关系
    which_driver_pool = int(cmdopt)
    driver = set_driver_pool
    # LoginPage(driver).pass_word_login(set_device_id_list[which_driver_pool], '\"baby_300\"', '\"aaaaaa\"')
    home_page = HomePage(driver)
    home_page.begin_home_page()
    assert home_page.is_element_exist('首页')


@allure.story('搜索页')
def test_Func_01_01_0003(set_device_id_list, set_driver_pool, cmdopt):
    # pool 池中 driver 与 device_id 为一对一的关系
    which_driver_pool = int(cmdopt)
    driver = set_driver_pool
    # LoginPage(driver).pass_word_login(set_device_id_list[which_driver_pool], '\"baby_300\"', '\"aaaaaa\"')
    home_page = HomePage(driver)
    print('home_page', home_page)
    search_page = home_page.to_search_page()
    print('page_source', search_page)
    search_page.search_class()
    assert search_page.is_element_exist('搜索')
