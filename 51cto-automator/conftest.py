# coding: utf-8


'''
全局配置
'''
import logging
import multiprocessing
import os
import time

import xlrd
import pytest
import yaml
from appium import webdriver

# from drivers.android import device_android
from lib.device_data import keep_port_available, start_appium, get_platform_version, start_devices
from lib.loggers import log


script_path_up = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_data_path = script_path_up + '/51cto-automator/data/case_data.yml'
test_case_data = yaml.safe_load(open(case_data_path, 'r'))
case_id_data_path = os.path.dirname(os.path.abspath(__file__)) + '/case/case_id.xlsx'
print('case_id_data_path', case_id_data_path)
MAX_POOL_NUMBER = 2
device_id_list = []


# 调用设备 ID 列表
@pytest.fixture(scope='session', autouse=True)
def set_device_id_list():
    device_id_list.clear()
    list1 = start_devices()
    for i in range(len(list1)):
        device_id_list.append(list1[i])
    return device_id_list


# 解析附加参数
def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="0", help="my option: 0 or 1"
    )


# 选择指令
@pytest.fixture(scope='session', autouse=True)
def cmdopt(request):
    return request.config.getoption("--cmdopt")


# 分发devicesID
@pytest.fixture
def deliver_event():
    wb = xlrd.open_workbook(filename=case_id_data_path)
    sheet1 = wb.sheet_by_index(0)
    case_id = sheet1.col_values(1)
    pool_id = sheet1.col_values(1)
    case_id.pop(0)
    pool_id.pop(0)
    return case_id, pool_id


# 设置驱动池
@pytest.fixture(scope='session', autouse=True)
def set_driver_pool(cmdopt):
    driver_pool = []
    device_id_list_num = len(device_id_list)
    real_pool_number = min(device_id_list_num, MAX_POOL_NUMBER)  # 人为控制设备运行数量
    port_id = 4724
    # bp_id = 99
    sys_port = 8200
    if device_id_list_num != 0:
        p = multiprocessing.Pool(real_pool_number)
        print(p)

    port_id = port_id + int(cmdopt)
    # bp_id = bp_id + int(cmdopt)
    sys_port = sys_port + int(cmdopt)
    keep_port_available(port_id)
    try:
        p.apply_async(start_appium, args=(port_id, device_id_list[int(cmdopt)],))
    except Exception as e:
        print(e, 11)
    # wait(10)
    time.sleep(3)
    plat_form_version = get_platform_version(device_id_list[int(cmdopt)])
    '''
    com.huawei.ohos.inputmethod
    '''

    caps = {'platformName': 'Android', 'platformVersion': plat_form_version, 'deviceName': 'nexus 6p',
            'newCommandTimeout': 0,
            'appPackage': 'com.cto51.student',
            'appActivity': '.foundation.activities.MainActivity',
            'systemPort': sys_port,
            'automationName': 'UiAutomator2',
            'disableSuppressAccessibilityService': True,
            'enableMultiWindows': True,
            'allowInvisibleElements': True,
            'ignoreUnimportantViews': False,
            'id': device_id_list[int(cmdopt)]}

    driver = webdriver.Remote('http://localhost:' + str(port_id) + '/wd/hub', caps)
    print('55555555555')
    print(driver)
    print('55555555555')
    driver.implicitly_wait(5)
    # 设置默认输入法
    # from page.main_page import MainPage
    print('11111')
    from page.login_page import LoginPage
    LoginPage(driver).pass_word_login(device_id_list[int(cmdopt)], '\"baby_300\"', '\"aaaaaa\"')
    # MainPage(driver).set_default_method().agree_gdpr().back_to_input_page()
    driver_pool.append(driver)
    # return driver_pool
    print('********  ********')
    print(driver_pool)
    print('********  ********')

    time.sleep(2)
    p.close()
    p.terminate()
    print('77777777777')
    print(driver_pool)
    print('77777777777')
    print(driver, "111111")
    return driver

    #
    #     try:
    #         p.apply_async(start_appium, args=(port_id, device_id_list[int(p)],))
    #     except Exception as e:
    #         print('报错喽---%s'%e)
    #     time.sleep(3)
    #     plat_form_version = get_platform_version(device_id_list[int(p)])
    #
    #     '''
    #     com.huawei.ohos.inputmethod
    #     '''
    #     try:
    #         caps = {'platformName': 'Android', 'platformVersion': plat_form_version, 'deviceName': 'nexus 6p',
    #                 'newCommandTimeout': 0,
    #                 'appPackage': 'com.xinmei365.emptyinput',
    #                 'appActivity': 'com.xinmei365.emptyinput.MainActivity',
    #                 'systemPort': sys_port,
    #                 'automationName': 'UiAutomator2',
    #                 'disableSuppressAccessibilityService': True,
    #                 'enableMultiWindows': True,
    #                 'allowInvisibleElements': True,
    #                 'ignoreUnimportantViews': False,
    #                 'id': device_id_list[int(i)]}
    #
    #         driver = webdriver.Remote('http://localhost:' + str(port_id) + '/wd/hub', caps)
    #         # driver = drivers.devices_driver.devs('http://localhost:' + str(port_id) + '/wd/hub', caps)
    #         driver.implicitly_wait(5)
    #         log.info(driver)
    #         driver_pool.append(driver)
    #         print(driver_pool,'000000')
    #         # return driver_pool
    #     except Exception as e:
    #         print('启动失败---%s'%e)
    #         # Log_info().getlog('start-drive-test-case').debug(e)
    # time.sleep(2)
    # p.close()
    # p.terminate()
    # yield driver_pool


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    set_driver_pool()
