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
from page.base_page import BasePage
from page.input_page import InputPage
from page.keyboard_setting_page import KeyboardSettingPage
from page.language_setting_page import LanguageSettingPage
from page.login_page import LoginPage
from page.page_setting_page import PageSettingPage
from page.sound_effect_page import SoundEffectPage
from page.theme_setting_page import ThemeSettingPage

from public.base_function import PATH

'''
生成allure报告 2 步：
1、python3 -m pytest testcase/TestCase1.py --alluredir report/allure_raw --clean-alluredir
2、allure generate report/allure_raw -o report/html --clean
'''

screen_size_list = []
test_case_data = get_path_data('/data/case_data.yml')
test_adb_data = get_path_data('/data/adb_data.yml')

# GDPR 弹窗相关控件
_gdpr_pop_up = (By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout')
_gdpr_disagree = (By.ID,'com.huawei.ohos.inputmethod:id/btn_deny')
_gdpr_agree = (By.ID,'com.huawei.ohos.inputmethod:id/btn_ok')
_gdpr_learn_more = (By.ID,'com.huawei.ohos.inputmethod:id/tv_content2')
_input_text_view = (By.CLASS_NAME, 'android.widget.EditText')
_message_input_box = (By.ID,'com.google.android.apps.messaging:id/compose_message_text')
_address_book_dialog = (By.ID,'com.android.packageinstaller:id/dialog_container')


@allure.story('检查字符点击与上屏功能-中文26键')
# 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
def test_InputMethod_SCB_Func_01_01_0002(set_device_id_list, set_driver_pool, cmdopt):
    # pool 池中 driver 与 device_id 为一对一的关系
    which_driver_pool = int(cmdopt)
    driver = set_driver_pool
    input_page = InputPage(driver)
    screen_size_list.clear()
    get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
    os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
    time.sleep(3)
    os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
    time.sleep(3)
    # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
    if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
                                 screen_size_list[1]) == 'english':
        print('当前为英文键盘')
        input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
    else:
        input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
        input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
    input_page.tap_menu()
    keyboard_setting_page = input_page.tap_setting()
    page_setting_page = keyboard_setting_page.to_page_setting_page()
    time.sleep(3)
    page_setting_page.check_number_capitalization('select')
    # from page.page_setting_page import PageSettingPage
    page_setting_page.back_to_setting_page().back_to_input_page()
    os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
    input_page.input_characters(test_case_data['func_01_01_01_0001']['word1'], set_device_id_list[which_driver_pool],
                                screen_size_list[0], screen_size_list[1])
    input_page.input_characters('1234567890', set_device_id_list[which_driver_pool],
                                screen_size_list[0], screen_size_list[1])
    text = input_page.find_element_by_class("android.widget.EditText").text
    print(text)
    # log.info(text,"这是日志")
    assert text == 'qwertyuiopasdfghjklzxcvbnm 1234567890 '
    input_page.return_to_launcher(set_device_id_list[which_driver_pool])



@allure.story('检查字符点击与上屏功能[一些符号上屏失败，需调研]')
# 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
def test_InputMethod_SCB_Func_01_01_0003(set_device_id_list, set_driver_pool, cmdopt):
    # pool 池中 driver 与 device_id 为一对一的关系
    which_driver_pool = int(cmdopt)
    input_page = InputPage(set_driver_pool)
    screen_size_list.clear()
    get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
    os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
    time.sleep(1)
    os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
    time.sleep(3)
    # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
    if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
                                 screen_size_list[1]) == 'chinese':
        print('当前为英文键盘')
        input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
    else:
        input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
        input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
                                    screen_size_list[1])
    input_page.tap_menu()
    input_page.tap_setting()
    # 关闭数字行
    KeyboardSettingPage(set_driver_pool).to_page_setting_page().check_number_capitalization('noselect')
    PageSettingPage(set_driver_pool).back_to_setting_page().back_to_input_page()
    time.sleep(2)
    os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
    # 进入符号页面
    input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
    time.sleep(2)
    input_page.click_symbol_keyboard('中文')
    input_page.click_symbol_keyboard('锁住')
    # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
    input_page.click_symbol_keyboard('\u3002')
    text = input_page.find_element_by_class("android.widget.EditText").text
    print(text)
    log.info(text,'我的报告2')
    assert text == '，。？！、：；……“”‘’@～—＃＊｜（）'
    # input_page.return_to_launcher(set_device_id_list[which_driver_pool])

#
# @allure.story('检查换行键功能')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0006(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         光标换行，有什么好的方法
#     '''
#     pass
#
#
# @allure.story('检查空格键功能使用')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0010(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     # 关闭数字行
#     KeyboardSettingPage(set_driver_pool).to_page_setting_page().check_number_capitalization('noselect')
#     PageSettingPage(set_driver_pool).back_to_setting_page().back_to_input_page()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.input_characters('nihao', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '你好'
#
#
# @allure.story('切换至符号页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0014(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     # 进入符号页面
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     time.sleep(2)
#     # 判断是否进入符号页面
#     input_page.is_element_exist('中文')
#     input_page.is_element_exist('\u3002')
#     input_page.click_symbol_keyboard('返回')
#     # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '去'
#
#
# @allure.story('逗号检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0053(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters(',', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.long_press(',', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '，！'
#
#
# @allure.story('空格检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0054(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         输入状态：目前自己实现的输入逻辑是在输入字母后，自动点击空格，是一个连贯的过程，所以单独的输入状态不好找
#     '''
#     pass
#
#
# @allure.story('句号检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0055(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters('.', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.long_press('.', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '。？'
#
#
# @allure.story('切换至普通符号页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_02_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#
#     # 进入符号页面
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     time.sleep(2)
#     # 判断是否进入符号页面
#     input_page.is_element_exist('中文')
#     input_page.is_element_exist('\u3002')
#     input_page.click_symbol_keyboard('返回')
#     # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '去'
#     # 还原至26键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#
#
# @allure.story('检查字符点击与上屏功能-英文键盘')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_03_0002(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         疑问细节：分别点击键盘中所有字母和阿拉伯数字键，点击数字键？
#     '''
#     pass
#
#
# @allure.story('检查符号点击与上屏功能-26键英文键盘')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_03_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_symbol')
#     input_page.input_characters('@#$%&-+()/:;!?_.', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('asterisk', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('single-quotation', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('quotation', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_en')
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '@#$%&-+()/:;!?_.*\'\"\")'
#
#
# @allure.story('手写识别体验')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_04_0010(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         手写how to do？
#     '''
#     pass
#
#
# @allure.story('笔画检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_05_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     time.sleep(2)
#     input_page.input_characters('一丨丿丶ㄥ通配', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '权'
#
#
# @allure.story('检查26键【?123】功能键显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0001(set_device_id_list, set_driver_pool, cmdopt):
#     '''检查符号键样式'''
#     pass
#
#
# @allure.story('点击【123】功能键盘检查键盘显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     # 手写
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_handwriting = input_page.screenshot2('手写-num')
#     # 笔画
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_bihua = input_page.screenshot2('笔画-num')
#     # 9键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_9key = input_page.screenshot2('9-num')
#     # 26键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_26key = input_page.screenshot2('26-num')
#     result1 = input_page.compare(pic_handwriting, pic_bihua)
#     result2 = input_page.compare(pic_bihua, pic_9key)
#     result3 = input_page.compare(pic_9key, pic_26key)
#     '''
#         截图比较
#     '''
#
#
# @allure.story('点击数字键盘任意按键检查字符上屏显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0009(set_device_id_list, set_driver_pool, cmdopt):
#     """
#         左侧符号控件的滑动点击
#     """
#
#
# @allure.story('检查符号页面分组显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0033(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     test_layout_list = ['手写键盘']  # , '笔画', '9键', '26键'
#     for layout in test_layout_list:
#         input_page.tap_menu()
#         input_page.tap_keyboard_layout()
#         input_page.to_which_keyboard_layout(layout)
#         input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         first_element_bounds_str = input_page.find_element_by_xpath('//*[@resource-id="com.huawei.ohos.inputmethod:id'
#                                                                     '/symbols_rcv"]/android.widget.LinearLayout['
#                                                                     '1]').get_attribute('bounds')
#         first_element_bounds = re.findall(r'\d+', first_element_bounds_str)
#         test_list = ['常用', '中文', '英文', '网络', '特殊', '数学', '序号', '日文', '希腊文', '藏文', '俄文', '拉丁文', '注音', '部首', '制表']
#         for i in test_list:
#             input_page.symbol_grouping_bar(i, 'left')
#             input_page.touch_tap((int(first_element_bounds[0]) + int(first_element_bounds[2])) / 2,
#                                  (int(first_element_bounds[1]) + int(first_element_bounds[3])) / 2)
#         input_page.click_symbol_keyboard('返回')
#
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '，，,@☆+①アαༀаÄā丨╭'
#     '''
#         流程能走通，但结果如何去检测？
#     '''
#
#
# @allure.story('点击语音输入键，语音输入')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_07_0036(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.voice_input('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                            screen_size_list[1])
#     os.system('say 你好')
#     time.sleep(3)
#     input_page.menu_back()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '你好。'
#
#
# @allure.story('中文九键键盘下显示验证码')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_08_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#         短信验证码相关验证
#     '''
#
#
# @allure.story('不同APP显示短信验证码-01')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_08_0019(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#         短信验证码相关验证
#     '''
#
#
# @allure.story('剪贴板内容最多显示5条')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0007(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.input_characters('nihaozhelishibeijing', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.clean_text()
#     input_page.tap_menu()
#     input_page.tap_edit()
#     operation_list1 = ['句首', '选择', 'right', 'right', '复制']
#     for operate1 in operation_list1:
#         input_page.edit_operation(operate1)
#     operation_list2 = ['选择', 'right', 'right', '复制']
#     for operate2 in operation_list2:
#         input_page.edit_operation(operate2)
#     operation_list3 = ['选择', 'right', '复制']
#     for operate3 in operation_list3:
#         input_page.edit_operation(operate3)
#     operation_list4 = ['选择', 'right', 'right', '复制']
#     for operate4 in operation_list4:
#         input_page.edit_operation(operate4)
#     operation_list5 = ['全选', '复制']
#     for operate5 in operation_list5:
#         input_page.edit_operation(operate5)
#     input_page.menu_back()
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     num = input_page.get_clipboard_num()
#     assert num == '(5/5)'
#     assert not input_page.is_element_exist('使用剪贴板以轻松粘贴文本')
#
#
# @allure.story('点击剪贴板复制内容可上屏')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0009(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     input_page.paste_clipboard_item()
#
#
# @allure.story('点击删除键，此内容消失')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0026(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     str1 = input_page.delete_clipboard_item()
#     assert str1 == '(0/5)'
#
#
# @allure.story('使用外接键盘输入字符能够正常展示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_12_0005(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     '''
#         外接键盘
#     '''
#
#
# @allure.story('使用虚拟键盘输入字符能够正常展示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_12_0006(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     '''
#         外接键盘
#     '''
#
#
# @allure.story('切换系统分辨率查看帐号登录状态')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_02_0032(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     time.sleep(1)
#     login_page.switch_wm_size(set_device_id_list[which_driver_pool], '800x1760')
#     time.sleep(1)
#     # 检验登录状态：1.非登录状态下，页面不存在'登录华为账号'关键字，页面底部没有'退出登录'按钮
#     # 检验细节：切换分辨率后，各控件点击后，响应是否正常
#     assert not login_page.is_element_exist('登录华为账号')
#     assert login_page.is_element_exist('退出登录')
#     theme_setting_page = login_page.my_skins()
#     time.sleep(1)
#     assert theme_setting_page.is_element_exist('皮肤')
#     theme_setting_page.back_to_previous_page()
#     font_setting_page = login_page.my_fonts()
#     time.sleep(1)
#     assert font_setting_page.is_element_exist('字体')
#     font_setting_page.back_to_previous_page()
#     sync_thesaurus_page = login_page.my_sync()
#     time.sleep(1)
#     assert sync_thesaurus_page.is_element_exist('同步词库')
#     sync_thesaurus_page.back_to_previous_page()
#     back_up_page = login_page.my_back_up()
#     time.sleep(1)
#     assert back_up_page.is_element_exist('备份设置项')
#     back_up_page.back_to_previous_page()
#     keyboard_setting_page = login_page.to_setting_page()
#     time.sleep(1)
#     assert keyboard_setting_page.is_element_exist('小艺输入法')
#     keyboard_setting_page.back_to_previous_page()
#     login_page.log_out('取消')
#     login_page.log_out('继续退出')
#     time.sleep(3)
#     assert login_page.is_element_exist('登录华为帐号')
#     # print('login_page:', login_page.driver.page_source)
#     login_page.log_in('取消')
#     login_page.switch_wm_size(set_device_id_list[which_driver_pool], 'reset')
#     time.sleep(3)
#     assert not login_page.is_element_exist('登录华为账号')
#     assert login_page.is_element_exist('退出登录')
#
#
# @allure.story('已登录帐号进入云备份设置页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_01_0004(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     time.sleep(1)
#     login_page.log_out('继续退出')
#     time.sleep(1)
#     login_page.log_in('取消')
#     time.sleep(1)
#     back_up_page = login_page.my_back_up()
#     time.sleep(1)
#     assert back_up_page.is_element_exist('备份设置项')
#     back_up_page.back_to_previous_page()
#
#
# @allure.story('已登录帐号进入云备份设置页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_01_0017(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     back_up_page = login_page.my_back_up()
#     back_up_page.restore_setting('确定')
#     back_up_page.back_to_previous_page()
#
#
# @allure.story('手动同步词库图标状态-同步完成01')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_02_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     sync_thesaurus_page = login_page.my_sync()
#     time.sleep(1)
#     sync_thesaurus_page.sync_thesaurus()
#     current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
#     print(current_time)
#     str_time = sync_thesaurus_page.get_sync_time()
#     print('str_time:', str_time)
#     assert current_time == str_time
#
#
# @allure.story('在语音输入页点击Menu进入菜单页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     assert input_page.is_element_exist('键盘布局')
#     '''
#     # 切换至横屏
#     input_page.rotate_the_screen_to_horizontal()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     '''
#
#
# @allure.story('使用普通话进行语音输入无异常')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     input_page.voice_change_language('普通话')
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     os.system('say 你好')
#     text = input_page.find_element_by_id('com.android.mms:id/embedded_text_editor').text
#     assert text == '你好。'
#
#
# @allure.story('使用粤语普通话免切换方言进行语音输入反馈无异常')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0015(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     input_page.voice_change_language('粤语')
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#
#     os.system('say -v Sin-ji 你好')
#     text = input_page.find_element_by_id('com.android.mms:id/embedded_text_editor').text
#     assert text == '你好。'
#
#
# @allure.story('添加语言确定恢复默认设置，语言页无变化')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0017(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     language_setting_page = keyboard_setting_page.to_language_setting_page()
#     language_setting_page.add_language_list2('南非荷兰文', 'af')
#     setting_page = language_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     language_setting_page = setting_page.to_language_setting_page()
#     status = language_setting_page.check_the_language_states('南非荷兰文')
#     # 通过语言item勾选状态以此判断是否存在'添加语言'中
#
#     assert status == 'true'
#
#
# @allure.story('在普通模式改变皮肤确定恢复默认设置，恢复成默认皮肤')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0022(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     theme_setting_page = keyboard_setting_page.to_theme_setting_page()
#     theme_setting_page.switch_theme('默认')
#     theme_setting_page.switch_theme('墨绿色')
#     theme_setting_page.switch_theme('浅艾蓝')
#     theme_selected = theme_setting_page.search_selected_theme()
#     assert theme_selected == '浅艾蓝'
#     setting_page = theme_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     setting_page.to_theme_setting_page()
#     theme_selected2 = theme_setting_page.search_selected_theme()
#     assert theme_selected2 == '默认'
#
#
# @allure.story('非默认字体确定恢复默认设置，字体页无变化')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0026(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     font_setting_page = keyboard_setting_page.to_font_setting_page()
#     font_data_list = ['系统字体', '鸿蒙字体', 'MidoRound', 'Joker', 'AriaSlab']
#     font_setting_page.change_font(font_data_list)
#     font_selected = font_setting_page.search_selected_font()
#     assert font_selected == 'AriaSlab'
#     setting_page = font_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     setting_page.to_font_setting_page()
#     font_selected2 = font_setting_page.search_selected_font()
#     assert font_selected2 == 'AriaSlab'
#
#
# @allure.story('打开一个模糊拼音选项确定恢复默认设置，选项恢复成默认全部关闭')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0041(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     fuzzy_pinyin_test_list = ['z = zh', 'c = ch', 'k = g']
#     chinese_setting_page.fuzzy_pinyin(fuzzy_pinyin_test_list)
#     status1 = chinese_setting_page.get_fuzzy_pinyin_status('z = zh')
#     status2 = chinese_setting_page.get_fuzzy_pinyin_status('c = ch')
#     status3 = chinese_setting_page.get_fuzzy_pinyin_status('k = g')
#     assert status1 == 'true'
#     assert status2 == 'true'
#     assert status3 == 'true'
#     # 退出模糊拼音页面
#     chinese_setting_page.back_to_previous_page()
#     # 退出中文设置页面
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     status = chinese_setting_page2.get_all_fuzzy_pinyin_status()
#     print(type(status), status)
#     assert status[0] == 10
#
#
# @allure.story('关闭拼音云输入确定恢复默认设置，拼音云输入开关打开')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0045(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     chinese_setting_page.chinese_setting_about_input('拼音云输入', '关闭')
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     status = chinese_setting_page2.get_all_status_in_chinese_setting('拼音云输入')
#     assert status == '开启'
#
#
# @allure.story('选择非关闭双拼输入选项确定恢复默认设置，选项恢复成默认关闭')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0049(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     chinese_setting_page.shuangpin_input('智能ABC')
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     text = chinese_setting_page2.get_shuangpin_input_text()
#     assert text == '关闭'
#
#
# @allure.story('关闭启用表情符号预测确定恢复默认设置，启用表情符号预测开关打开')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0065(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     input_setting_page.click_which_item('启用表情符号预测', 'none')
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     status = input_setting_page2.check_item_status('启用表情符号预测')
#     assert status == 'true'
#
#
# @allure.story('入口-设置')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_03_02_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.return_to_launcher(set_device_id_list[which_driver_pool])
#     input_page.find_element_by_xpath('//android.widget.TextView[@content-desc="小艺输入法"]').click()
#     from page.login_page import LoginPage
#     login_page = LoginPage(set_driver_pool)
#     setting_page = login_page.to_setting_page()
#     page_setting_page = setting_page.to_page_setting_page()
#     change_font_size_page = page_setting_page.change_font_size()
#     assert change_font_size_page.is_element_exist('字体大小')
#
#
#
#
# @allure.story('页面测试')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_test1(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     setting_page = input_page.tap_setting()
#     page_setting_page = setting_page.to_page_setting_page()
#     page_setting_page.button_long_press_delay(0.3, '取消')
#     page_setting_page.button_long_press_delay(0.01, '取消')
#     page_setting_page.button_long_press_delay(0.7, '默认')
#     page_setting_page.button_long_press_delay(0.99, '确定')
#
#
# @allure.story('查看语音长文本模式显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_horizontal_and_vertical_01(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_setting().to_voice_setting_page()
#     from page.voice_setting_page import VoiceSettingPage
#     voice_setting_page = VoiceSettingPage(set_driver_pool)
#     status = voice_setting_page.get_extended_dictation_status()
#     assert status == 'false'
#
#
# @allure.story('检查首字母大写功能')
# def test_InputMethod_SCB_Func_01_01_01_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(
#         test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     input_page.find_element_by_id_click('com.google.android.apps.messaging:id/compose_message_text')
#     # 有的手机首次调起键盘后，可能会弹起'获取联系人权限'的系统弹框
#     # os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(2)
#     input_page.find_element_by_id_click(
#         'com.android.mms:id/embedded_text_editor')  # com.google.android.apps.messaging:id/compose_message_text
#     if input_page.find_element_by_id('com.android.packageinstaller:id/dialog_container'):
#         input_page.find_element_by_id_click('com.android.packageinstaller:id/permission_allow_button')
#         input_page.find_element_by_id_click('com.google.android.apps.messaging:id/compose_message_text')
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.input_characters(test_case_data['func_01_01_01_0003']['word'], set_device_id_list[which_driver_pool],
#                                 screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_id('com.android.mms:id/embedded_text_editor').text
#     assert text == 'Qwerty '
#     input_page.return_to_launcher(set_device_id_list[which_driver_pool])
#
#
# @allure.story('检查大小写切换键功能-大写锁定')
# def test_InputMethod_SCB_Func_01_01_01_0008(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     pic_before = input_page.screenshot2('pic1')
#     input_page.input_characters('shift', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.input_characters('shift', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     pic_after = input_page.screenshot2('pic2')
#     input_page.input_characters('hello', set_device_id_list[which_driver_pool],
#                                 screen_size_list[0], screen_size_list[1])
#     input_page.input_characters(',', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.input_characters('world', set_device_id_list[which_driver_pool],
#                                 screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     result = input_page.compare(pic_before, pic_after)
#     print(result)
#     print(text)
#     assert text == 'HELLO ,WORLD '
#
#
# @allure.story('检查按键点击与上屏功能')
# def test_InputMethod_SCB_Func_01_01_01_0009(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters('abcdef', set_device_id_list[which_driver_pool],
#                                 screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == 'abcdef '
#
#
# @allure.story('检查长按弹泡功能')
# def test_InputMethod_SCB_Func_01_01_01_00010(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     time.sleep(1)
#     KeyboardSettingPage(set_driver_pool).to_page_setting_page().check_bubble_capitalization('noselect')
#     PageSettingPage(set_driver_pool).back_to_setting_page().back_to_input_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     '''
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     from page.language_setting_page import LanguageSettingPage
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.uncheck_language_list('中文')
#     language_setting_page.back_to_previous_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     '''
#     input_page.long_press('qwertyuiopasdfghjklzxcvbnm', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '1234567890@#$%&-+()*\"\':;!?'
#
#
# @allure.story('检查空格键功能使用')
# def test_InputMethod_SCB_Func_01_01_01_00011(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters('hello', set_device_id_list[which_driver_pool],
#                                 screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == 'hello '
#
#
# @allure.story('检查空格键功能使用')
# def test_InputMethod_SCB_Func_01_01_01_00013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.long_press('space', set_device_id_list[which_driver_pool],
#                           screen_size_list[0], screen_size_list[1])
#     input_page.deal_sys_dialog('//*[@resource-id="com.android.packageinstaller:id/permission_message"', '允许')
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.long_press('space', set_device_id_list[which_driver_pool],
#                           screen_size_list[0], screen_size_list[1])
#     assert input_page.is_element_exist('语言选择按键，双击选择键盘语言') is True
#     input_page.menu_back()
#
#
# @allure.story('检查句号长按弹泡功能')
# def test_InputMethod_SCB_Func_01_01_01_00016(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#     英文键盘长按，无其他可选符号，是否是版本差异
#     '''
#     pass
#
#
# @allure.story('中文键盘检查语言切换键')
# def test_InputMethod_SCB_Func_01_01_01_00036(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     # 26键点击中/英切换键
#     # 英文键盘
#     pic_26_english = input_page.screenshot2('26键英文')
#     pic_26_english_path = PATH(os.getcwd() + "/testcase/TestResult/26键英文.png")
#     result_26_english = input_page.compare(pic_26_english_path, pic_26_english)
#     pytest.assume(result_26_english == 0.0)
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     pytest.assume(text == 'q ')
#     # 点击中/英切换键，检查是否为中文键盘
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_26_chinese = input_page.screenshot2('26键中文')
#     pic_26_chinese_path = PATH(os.getcwd() + "/testcase/TestResult/26键中文.png")
#     result_26_chinese = input_page.compare(pic_26_chinese_path, pic_26_chinese)
#     pytest.assume(result_26_chinese == 0.0)
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     pytest.assume(text == '去')
#     # 进入键盘布局，切换为 9 键
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#     pic_9 = input_page.screenshot2('9键中文')
#     pic_9_path = PATH(os.getcwd() + "/testcase/TestResult/9键中文.png")
#     result_9 = input_page.compare(pic_9_path, pic_9)
#     pytest.assume(result_9 == 0.0)
#     input_page.input_characters('a', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     pytest.assume(text == '啊')
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     # 使用英文布局
#     golVar.set_value('language_layout', 'relative_layout_en')
#     # 切换为英文键盘，清空输入框
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     pytest.assume(text == 'q ')
#     # 进入键盘布局，切换为笔画
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     pic_bihua = input_page.screenshot2('笔画中文')
#     pic_bihua_path = PATH(os.getcwd() + "/testcase/TestResult/笔画中文.png")
#     result_bihua = input_page.compare(pic_bihua_path, pic_bihua)
#     pytest.assume(result_bihua == 0.0)
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_en')
#     # 切换为英文键盘，清空输入框
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     # 进入键盘布局，切换为手写
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     pic_shouxie = input_page.screenshot2('手写中文')
#     pic_shouxie_path = PATH(os.getcwd() + "/testcase/TestResult/手写中文.png")
#     result_shouxie = input_page.compare(pic_shouxie_path, pic_shouxie)
#     pytest.assume(result_shouxie == 0.0)
#     # 切换为英文键盘，清空输入框
#     # 进入语言添加页面，添加语言
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_en')
#     input_page.language_picker_list('更多语言...')
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.add_language_list2('中文', 'zh_HK')
#     language_setting_page.add_language_list2('中文', 'zh_TW')
#     language_setting_page.back_to_previous_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     golVar.set_value('language_layout', '注音')
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     # 添加注音键盘
#     input_page.language_picker_list('中文（注音）')
#     pic_zhuyin = input_page.screenshot2('注音中文')
#     pic_zhuyin_path = PATH(os.getcwd() + "/testcase/TestResult/注音中文.png")
#     result_zhuyin = input_page.compare(pic_zhuyin_path, pic_zhuyin)
#     pytest.assume(result_zhuyin == 0.0)
#     # 添加仓颉键盘
#     # golVar.set_value('language_layout', '仓颉')
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('中文（倉頡）')
#     pic_cangjie = input_page.screenshot2('倉頡中文')
#     pic_cangjie_path = PATH(os.getcwd() + "/testcase/TestResult/倉頡中文.png")
#     result_cangjie = input_page.compare(pic_cangjie_path, pic_cangjie)
#     pytest.assume(result_cangjie == 0.0)
#
#
# @allure.story('单手键盘初始状态和基础功能检查')
# def test_InputMethod_SCB_Func_01_02_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 清除输入法数据
#     os.system('adb -s %s shell pm clear com.huawei.ohos.inputmethod' % set_device_id_list[which_driver_pool])
#     input_page.set_default_inputmethod('ziyan')
#     time.sleep(3)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.deal_gdpr_informal()
#     time.sleep(2)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('单手模式')
#     input_page.switch_keyboard_to_opposite()
#     input_page.return_to_normal()
#
#
# @allure.story('检查悬浮键盘模式各功能使用')
# def test_InputMethod_SCB_Func_01_03_0010(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     # 进入悬浮键盘模式
#     input_page.to_which_keyboard_mode('悬浮键盘')
#     time.sleep(2)
#     # 依次按上、左、右、下 4 个方向移动悬浮键盘
#     input_page.float_to_move('up', 100)
#     input_page.float_to_move('left', 100)
#     input_page.float_to_move('right', 100)
#     input_page.float_to_move('down', 100)
#     # 隐藏键盘后再调起键盘
#     input_page.menu_back()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     # 点击 menu
#     input_page.tap_menu()
#     # 切换键盘布局：手写键盘、9键、笔画、26键
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     # 点击进入主题，改变主题，换第一套然后回到输入页面
#     input_page.tap_menu()
#     input_page.change_theme().switch_them1()
#     ThemeSettingPage(set_driver_pool).back_to_previous_page()
#     ThemeSettingPage(set_driver_pool).back_to_previous_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     # 编辑键盘，改动大小
#
#     input_page.tap_menu()
#     input_page.tap_adjust_size()
#     input_page.adjust_size('a', 'up', 100, screen_size_list[0], screen_size_list[1])
#     input_page.adjust_size('b', 'down', 100, screen_size_list[0], screen_size_list[1])
#     input_page.adjust_size('c', 'left', 100, screen_size_list[0], screen_size_list[1])
#     input_page.adjust_size('d', 'right', 100, screen_size_list[0], screen_size_list[1])
#     input_page.float_finish_resize()
#     # 编辑键盘恢复默认大小
#     input_page.tap_menu()
#     input_page.tap_adjust_size()
#     input_page.float_restore_default()
#     # 点击剪切板，粘贴第一条内容
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     input_page.clipboard_func(1, '粘贴')
#     input_page.menu_back()
#     # 点击编辑按钮，并进行相关操作
#     input_page.tap_menu()
#     input_page.tap_edit()
#     input_page.edit_operation('全选')
#     input_page.edit_operation('剪切')
#     input_page.edit_operation('粘贴')
#     input_page.edit_operation('句首')
#     input_page.edit_operation('句尾')
#     input_page.edit_operation('句首')
#     input_page.edit_operation('选择')
#     input_page.edit_operation('right')
#     input_page.edit_operation('复制')
#     input_page.edit_operation('粘贴')
#     input_page.edit_operation('删除')
#     input_page.edit_operation('回车')
#     input_page.edit_operation('剪切板')
#     input_page.clipboard_func(1, '粘贴')
#     input_page.menu_back()
#     # 声音振动调节
#     input_page.tap_menu()
#     input_page.tap_sound_vibration()
#     input_page.adjust_vibration(1)
#     input_page.adjust_vibration(0.5)
#     input_page.adjust_vibration(0.01)
#     input_page.adjust_sound(1)
#     input_page.adjust_sound(0.5)
#     input_page.adjust_sound(0.01)
#     input_page.enter_keyboard_sound_page()
#     SoundEffectPage(set_driver_pool).switch_sound9().back_to_previous_page()
#     SoundEffectPage(set_driver_pool).back_to_previous_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     time.sleep(2)
#
#     KeyboardSettingPage(set_driver_pool).back_to_previous_page()
#
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.float_to_normal()
#
#
# @allure.story('检查键盘初始状态和基础功能')
# def test_InputMethod_SCB_Func_01_04_0002(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 清除输入法数据
#     os.system('adb -s %s shell pm clear com.huawei.ohos.inputmethod' % set_device_id_list[which_driver_pool])
#     input_page.set_default_inputmethod('ziyan')
#     time.sleep(5)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.deal_gdpr_informal()
#     time.sleep(5)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('拇指模式')
#     pic_muzhi = PATH(os.getcwd() + "/testcase/TestResult/拇指键盘.png")
#     pic = input_page.screenshot2('拇指键盘')
#     result = input_page.compare(pic_muzhi, pic)
#     assert result == 0.0
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('普通键盘')
#
#
# @allure.story('使用外接键盘输入字符能够正常展示')
# def test_InputMethod_SCB_Func_01_05_0005(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#         外界键盘？？？
#     '''
#
#
# @allure.story('显示一元联想词语言确认')
# def test_InputMethod_SCB_Func_01_05_0034(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#             外接键盘？？？
#     '''
#
#
# @allure.story('简体中文支持手写键盘')
# def test_InputMethod_SCB_Func_01_07_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     else:
#         print('当前为中文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     pic_muzhi = PATH(os.getcwd() + "/testcase/TestResult/手写中文.png")
#     pic = input_page.screenshot2('手写键盘')
#     result = input_page.compare(pic_muzhi, pic)
#     assert result == 0.0
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#
#
# @allure.story('麦克风权限默认禁止')
# def test_InputMethod_SCB_Func_01_08_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     # 进入华为手机系统设置页面
#     os.system('adb -s %s shell am start com.android.settings/.HWSettings' %
#               set_device_id_list[which_driver_pool])
#
#     base_page = BasePage(set_driver_pool)
#     # 点击'设置'中的应用
#     base_page.scroll_syspage_to_find('//*[@resource-id="com.android.settings:id/main_content"]', '应用')
#     # 点击应用页面中的应用管理
#     base_page.click_syspage_app_management()
#     # 寻找应用管理页面中的'小艺输入法'
#     base_page.scroll_syspage_to_find('//*[@resource-id="android:id/list"]', '小艺输入法')
#     # 点击'权限'
#     base_page.click_syspage_app_info()
#     # 若已禁止，则授予麦克风权限
#     if base_page.is_element_exist('已禁止'):
#         assert base_page.is_element_exist('麦克风')
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     assert input_page.is_element_exist('禁止')
#
#
# @allure.story('点击设置，允许麦克风权限，进入语音键盘')
# def test_InputMethod_SCB_Func_01_08_0005(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.find_element_by_text_click('禁止后不再提示')
#     # 进入华为手机系统设置页面
#     os.system('adb -s %s shell am start com.android.settings/.HWSettings' %
#               set_device_id_list[which_driver_pool])
#
#     base_page = BasePage(set_driver_pool)
#     # 点击'设置'中的应用
#     base_page.scroll_syspage_to_find('//*[@resource-id="com.android.settings:id/main_content"]', '应用')
#     # 点击应用页面中的应用管理
#     base_page.click_syspage_app_management()
#     # 寻找应用管理页面中的'小艺输入法'
#     base_page.scroll_syspage_to_find('//*[@resource-id="android:id/list"]', '小艺输入法')
#     # 点击'权限'
#     base_page.click_syspage_app_info()
#     # 若已禁止，则授予麦克风权限
#     if base_page.is_element_exist('已禁止'):
#         base_page.click_syspage_universal('麦克风')
#         base_page.click_syspage_universal('仅使用期间允许')
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     # 通过语音页面中的控件'语言选择按键，双击选择键盘语言'判断当前页面是否是语音属入页面
#     assert input_page.is_element_exist('语言选择按键，双击选择键盘语言')
#
#
# @allure.story('语音功能入口')
# def test_InputMethod_SCB_Func_01_08_0006(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     '''
#         此处需改为华为短信页面
#     '''
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 长按空格调出语音输入界面
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.deal_sys_dialog('要允许小艺输入法录制音频吗？', '允许')
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     pic_yuyin = PATH(os.getcwd() + "/testcase/TestResult/语音界面.png")
#     pic = input_page.screenshot2('语音界面')
#     result = input_page.compare(pic_yuyin, pic)
#     assert result < 2
#
#
# @allure.story('输入emoji，无异常')
# def test_InputMethod_SCB_Func_01_09_0002(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.input_characters('emjo', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     time.sleep(3)
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print('text:', text)
#     assert text == '😀'
#
#
# @allure.story('使用编辑键盘时，键盘功能全部置灰')
# def test_InputMethod_SCB_Func_02_02_02_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_adjust_size()
#     pic_bianji = PATH(os.getcwd() + "/testcase/TestResult/编辑键盘.png")
#     pic = input_page.screenshot2('编辑键盘')
#     result = input_page.compare(pic_bianji, pic)
#     assert result < 2
#
#
# @allure.story('删除只有一种键盘布局的语言，该语言重新展示在可用语言列表中')
# def test_InputMethod_SCB_Func_03_01_01_0002(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     time.sleep(1)
#     input_page.tap_setting()
#
#     KeyboardSettingPage(set_driver_pool).to_language_setting_page()
#
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.open_input_menu_search('阿斯图里亚斯文')
#     language_num_1 = language_setting_page.get_list_total_num('//android.widget.ExpandableListView/android'
#                                                               '.widget.LinearLayout')
#     language_setting_page.uncheck_language_list('阿斯图里亚斯文')
#     if language_setting_page.check_the_language_states('阿斯图里亚斯文') == 'false':
#         print('取消：', language_setting_page.is_element_exist('删除语言按键，双击删除 阿斯图里亚斯文 语言'))
#         assert language_setting_page.is_element_exist('删除语言按键，双击删除 阿斯图里亚斯文 语言')
#     time.sleep(1)
#     language_setting_page.delete_language('阿斯图里亚斯文')
#     language_num_2 = language_setting_page.get_list_total_num('//android.widget.ExpandableListView/android'
#                                                               '.widget.LinearLayout')
#     print('num: ', int(language_num_1) - int(language_num_2))
#     assert int(language_num_1) - int(language_num_2) == 1
#     # language_setting_page.add_language_list2('阿斯图里亚斯文', 'ast')
#
#     # language_setting_page.return_to_launcher()
#
#
# @allure.story('进入语言页-键盘长按地球键')
# def test_InputMethod_SCB_Func_03_01_01_0010(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     assert language_setting_page.is_element_exist('语言')
#     # language_setting_page.return_to_launcher()
#
#
# @allure.story('进入语言页-键盘点击Menu')
# def test_InputMethod_SCB_Func_03_01_01_0011(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_setting()
#     KeyboardSettingPage(set_driver_pool).to_language_setting_page()
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     assert language_setting_page.is_element_exist('语言')
#     # language_setting_page.return_to_launcher()
#
#
# @allure.story('进入语言页-点击输入法桌面icon')
# def test_InputMethod_SCB_Func_03_01_01_0012(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0008']['ohos'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     KeyboardSettingPage(set_driver_pool).to_language_setting_page()
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     assert language_setting_page.is_element_exist('语言')
#     # language_setting_page.return_to_launcher()
#
#
# @allure.story('切换系统语言-系统语言需添加马来语')
# def test_InputMethod_SCB_Func_03_01_01_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     os.system(test_adb_data['adb_01_01_01_0009']['language_setting'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.to_system_language_picker('语言和地区', '马来文')
#     time.sleep(3)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('Lebih banyak bahasa...')
#     time.sleep(1)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     # 判断马来西亚语有勾选状态，以此来判断马来西亚语已添加至【添加语言】列表中
#     assert language_setting_page.check_the_language_states('Bahasa Melayu (Malaysia)')
#     os.system(test_adb_data['adb_01_01_01_0009']['language_setting'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 还原系统语言至中文
#     input_page.to_system_language_picker('Bahasa dan kawasan', 'Cina Ringkas')
#
#
# @allure.story('添加语言-同意隐私声明-连接WiFi')
# def test_InputMethod_SCB_Func_03_01_01_0015(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     time.sleep(3)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     # 添加南非荷兰语前，'添加语言'列表中 item 的数目
#     before_add_language = language_setting_page.get_list_total_num('//android.widget.ExpandableListView/android'
#                                                                    '.widget.LinearLayout')
#     if language_setting_page.is_element_exist('添加语言按键，双击添加 南非荷兰文 语言'):
#         language_setting_page.add_language_list2('南非荷兰文', 'af')
#     time.sleep(3)
#     # 添加南非荷兰语后，'添加语言'列表中 item 的数目，如果添加后的语言数目-添加前的语言数目=1，说明语言添加成功，在'添加语言'列表中
#     after_add_language = language_setting_page.get_list_total_num('//android.widget.ExpandableListView/android.widget'
#                                                                   '.LinearLayout')
#     if int(after_add_language) - int(before_add_language) == 1:
#         assert language_setting_page.check_the_language_states('南非荷兰文') == 'true'
#         language_setting_page.back_to_previous_page()
#         os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#         afrikaans_keyboard = PATH(os.getcwd() + "/testcase/TestResult/南非键盘.png")
#         pic = input_page.screenshot2('南非键盘')
#         result = input_page.compare(afrikaans_keyboard, pic)
#         assert result < 2
#
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('中文')
#
#
# @allure.story('语言布局切换')
# def test_InputMethod_SCB_Func_03_01_01_0025(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     time.sleep(3)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.updata_layout2('英语 (美国)', 2)
#     time.sleep(1)
#     language_setting_page.back_to_previous_page()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.input_characters('qwerty', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == 'qwertz '
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.screenshot_universal('layout', 2)
#     # input_page.return_to_launcher()
#
#
# @allure.story('存在多个已添加语言-停用单个语言')
# def test_InputMethod_SCB_Func_03_01_01_0046(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     time.sleep(3)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.uncheck_language_list('英语 (美国)')
#     time.sleep(1)
#     states = language_setting_page.check_the_language_states('英语 (美国)')
#     assert states == 'false'
#     time.sleep(1)
#     language_setting_page.is_element_exist('//android.widget.ImageView[@content-desc="删除语言按键，双击删除 %s 语言"]'
#                                            % '英语 (美国)')
#     time.sleep(1)
#     language_setting_page.back_to_previous_page()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     assert input_page.is_element_exist('英语 (美国)') is False
#
#
# @allure.story('【添加语言】中被勾选语言<5-添加语言')
# def test_InputMethod_SCB_Func_03_01_01_0053(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     time.sleep(3)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.add_language_list2('德语', 'de')
#     states = language_setting_page.check_the_language_states('德语')
#     assert states == 'true'
#
#
# @allure.story('【添加语言】中被勾选语言<5-启用单个语言')
# def test_InputMethod_SCB_Func_03_01_01_0051(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.language_picker_list('更多语言...')
#     time.sleep(3)
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.add_language_list2('西班牙语', 'es')
#     language_setting_page.add_language_list2('法语', 'fr')
#     language_setting_page.add_language_list2('俄语', 'ru')
#     language_setting_page.uncheck_language_list('西班牙语')
#     language_setting_page.uncheck_language_list('法语')
#     language_setting_page.uncheck_language_list('俄语')
#     # uncheck_language_list方法其实是点击checkbox，未选中时，点击则显示选中状态
#     language_setting_page.uncheck_language_list('德语')
#     assert language_setting_page.check_the_language_states('德语') == 'true'
#     time.sleep(1)
#     language_setting_page.back_to_previous_page()
#     input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     input_page.is_element_exist('德语') is True
#
#
# @allure.story('检查语言列表搜索入口')
# def test_InputMethod_SCB_Func_03_01_02_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     # 通过命令的方式启动输入法
#     os.system(test_adb_data['adb_01_01_01_0008']['ohos'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     KeyboardSettingPage(set_driver_pool).to_language_setting_page()
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.click_input_menu_search()
#     # 检查搜索框中是否出现'Search'文案，与清空按钮
#     if language_setting_page.is_element_exist('Search'):
#         if language_setting_page.is_element_exist('清空按键，双击清空搜索框内容'):
#             language_setting_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                                    screen_size_list[1])
#             text = language_setting_page.find_element_by_class("android.widget.EditText").text
#             assert text == '去'
#
#
# @allure.story('检查搜索语言逻辑及功能')
# def test_InputMethod_SCB_Func_03_01_02_0006(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_setting()
#     KeyboardSettingPage(set_driver_pool).to_language_setting_page()
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.click_input_menu_search()
#     # 检查搜索框中是否出现'Search'文案，与清空按钮
#     if language_setting_page.is_element_exist('Search'):
#         if language_setting_page.is_element_exist('清空按键，双击清空搜索框内容'):
#             input_page = InputPage(set_driver_pool)
#             input_page.long_press('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                   screen_size_list[1])
#             input_page.language_picker_list('English(United States)')
#             input_page.input_characters('p', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             # 目的：点击 back 键，收起键盘
#             # input_page.back_to_previous_page()
#             # text = input_page.find_element_by_class("android.widget.EditText").text
#             if language_setting_page.is_element_exist('Polski') is not True:
#                 print('当前页面不含Polski')
#             input_page.input_characters('olski', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             if language_setting_page.is_element_exist('Polski') is True:
#                 print('当前页面含有Polski')
#             # input_page.return_to_launcher()
#
#
# @allure.story('emoji候选展示')
# def test_InputMethod_SCB_Func_03_05_01_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     keyboard_setting_page = KeyboardSettingPage(set_driver_pool)
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     if input_setting_page.check_item_status('启用表情符号预测') is not True:
#         input_setting_page.click_which_item('启用表情符号预测')
#     input_setting_page.back_to_previous_page()
#     keyboard_setting_page.back_to_previous_page()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.input_characters('apple', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.click_which_candidate(3)
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '#127822;'
#
#
# @allure.story('快速插入联想词输入检查02')
# def test_InputMethod_SCB_Func_03_05_02_0015(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     keyboard_setting_page = KeyboardSettingPage(set_driver_pool)
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     if input_setting_page.check_item_status('快速插入联想词') is not True:
#         input_setting_page.click_which_item('快速插入联想词')
#     input_setting_page.back_to_previous_page()
#     keyboard_setting_page.back_to_previous_page()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.input_characters('test', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     # 获取 top1 的候选词
#     top_1 = input_page.find_candidate(2)
#     input_page.input_characters('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     # 查询 top1 的词是否在上屏的 text 中，如果在，则说明 test 上屏后，点击空格候选词也自动上屏
#     assert top_1 in text
#
#
# @allure.story('应用支持URL快捷键')
# def test_InputMethod_SCB_Func_03_05_02_0015(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     # os.system(test_adb_data['adb_01_01_01_0010']['opera_browser'] % set_device_id_list[which_driver_pool])
#     # time.sleep(1)
#     # input_page.click_browser_search_box('Opera')
#     # time.sleep(2)
#     os.system(test_adb_data['adb_01_01_01_0011']['chrome_browser'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.click_browser_search_box('Chrome')
#     time.sleep(3)
#     if input_page.is_element_exist('com.huawei.ohos.inputmethod:id/extra_container_top'):
#         pic = input_page.screenshot_urlboard('url')
#         url_keyboard = PATH(os.getcwd() + "/testcase/TestResult/url.png")
#         result = input_page.compare(url_keyboard, pic)
#         assert result < 2
#     input_page.click_url('url_www')
#     input_page.click_url('url_point')
#     input_page.click_url('url_slash')
#     input_page.click_url('url_com')
#     text = input_page.find_url_text('Chrome')
#     assert text == 'www../.com​'
#     input_page.click_url('left_layout')
#     input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text2 = input_page.find_url_text('Chrome')
#     assert text2 == 'www../.cm​'
#     input_page.click_url('right_layout')
#     input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text3 = input_page.find_url_text('Chrome')
#     assert text3 == 'www../.c'
#     # os.system(test_adb_data['adb_01_01_01_0012']['microsoft_browser'] % set_device_id_list[which_driver_pool])
#     # time.sleep(2)
#     # input_page.click_browser_search_box('MicroSoft')
#     # time.sleep(2)
#     # os.system(test_adb_data['adb_01_01_01_0013']['via_browser'] % set_device_id_list[which_driver_pool])
#     # time.sleep(1)
#     # input_page.click_browser_search_box('Via')
#     # time.sleep(2)
#     # os.system(test_adb_data['adb_01_01_01_0014']['firefox_browser'] % set_device_id_list[which_driver_pool])
#     # time.sleep(1)
#     # input_page.click_browser_search_box('FireFox')
#     # time.sleep(2)
#
#
# @allure.story('test')
# def test_InputMethod_SCB_Func_test(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     time.sleep(2)
#     # input_page.write_words()
#     input_page.write_words()
#
#
# @allure.story('打点测试，遍历 30 种键盘')
# def test_30(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0008']['ohos'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     keyboard_setting_page = KeyboardSettingPage(set_driver_pool)
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     input_setting_page.click_which_item('快速插入联想词')
#     input_setting_page.back_to_previous_page()
#     keyboard_setting_page.to_language_setting_page()
#     language_setting_page = LanguageSettingPage(set_driver_pool)
#     language_setting_page.add_language_list2('马来文 (马来西亚)', 'ms_my')
#     language_setting_page.add_language_list2('德文', 'de')
#     language_setting_page.add_language_list2('英文 (澳大利亚)', 'en_AU')
#     language_setting_page.add_language_list2('英文 (加拿大)', 'en_CA')
#     language_setting_page.add_language_list2('英文 (英国)', 'en_GB')
#     language_setting_page.add_language_list2('西班牙文', 'es')
#     language_setting_page.add_language_list2('西班牙文（拉丁美洲）', 'es_la')
#     # language_setting_page.add_language_list2('西班牙文 (美国)', 'es_us')
#     language_setting_page.add_language_list2('西班牙文 (墨西哥)', 'es_mx')
#     language_setting_page.add_language_list2('法文', 'fr')
#     language_setting_page.add_language_list2('法文 (加拿大)', 'fr_ca')
#     language_setting_page.add_language_list2('印度尼西亚文', 'id')
#     language_setting_page.add_language_list2('意大利文', 'it')
#     language_setting_page.add_language_list2('波兰语', 'pl')
#     language_setting_page.add_language_list2('葡萄牙文 (巴西)', 'pt_br')
#     language_setting_page.add_language_list2('葡萄牙文 (葡萄牙)', 'pt_pt')
#     language_setting_page.add_language_list2('土耳其文', 'tr')
#     language_setting_page.add_language_list2('捷克文', 'cs')
#     language_setting_page.add_language_list2('俄文', 'ru')
#     # language_setting_page.add_language_list2('乌尔都文', 'ur')
#     language_setting_page.add_language_list2('阿拉伯文', 'ar')
#     language_setting_page.add_language_list2('阿拉伯文 (阿尔及利亚)', 'ar_ar')
#     language_setting_page.add_language_list2('阿拉伯文(黎凡特)', 'ar_li')
#     language_setting_page.add_language_list2('阿拉伯文 (摩洛哥)', 'ar_mo')
#     language_setting_page.add_language_list2('阿拉伯文 (沙特阿拉伯)', 'ar_sa')
#     language_setting_page.add_language_list2('阿拉伯文 (突尼斯)', 'ar_tu')
#     language_setting_page.add_language_list2('阿拉伯文 (埃及)', 'ar_eg')
#     language_setting_page.add_language_list2('印地文', 'hi')
#     language_setting_page.add_language_list2('泰文', 'th')
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     # 拉起键盘
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#
#     input_page = InputPage(set_driver_pool)
#     input_page.deal_sys_dialog('通讯录', '允许')
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     language_list = ['ไทย', 'हिन्दी', 'العربية (مصر)', 'العربية (تونس)', 'العربية (المملكة العربية السعودية)',
#                      'العربية (المغرب)', 'العربية (الشرق)‎', 'العربية (الجزائر)', 'العربية', 'Русский',
#                      'Čeština', 'Türkçe', 'Português (Portugal)', 'Português (Brasil)', 'Polski', 'Melayu (Malaysia)',
#                      'Italiano', 'Indonesia', 'Français (Canada)', 'Français', 'Español(México)',
#                      'Español(América Latina)', 'Español', 'English(United States)',
#                      'English(United Kingdom)', 'English(Canada)', 'English(Australia)', 'Deutsch']
#     # language_list = ['हिन्दी', 'العربية (مصر)', 'Deutsch']
#     for language in language_list:
#         # if language in ['العربية (مصر)', 'العربية (تونس)', 'العربية (المملكة العربية السعودية)',
#         #              'العربية (المغرب)', 'العربية (الشرق)‎', 'العربية (الجزائر)', 'العربية', 'اردو']:
#         # 点击语言键
#
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         print('abc')
#         time.sleep(1)
#         input_page.language_picker_list(language)
#         os.system('adb shell input tap 540 1800')
#         os.system('adb shell input tap 540 1800')
#         # 点击删除键
#         input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         # 点击空格键
#         input_page.input_characters('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         os.system('adb shell input tap 540 1800')
#         # 点击回车键
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#         input_page.tap_menu()
#         input_page.tap_keyboard_mode()
#         input_page.to_which_keyboard_mode('单手模式')
#         input_page.tap_menu()
#         input_page.tap_keyboard_mode()
#         input_page.to_which_keyboard_mode('悬浮键盘')
#         input_page.tap_menu()
#         input_page.tap_keyboard_mode()
#         input_page.to_which_keyboard_mode('拇指模式')
#         input_page.tap_menu()
#         input_page.tap_keyboard_mode()
#         input_page.to_which_keyboard_mode('编辑键盘')
#         input_page.float_restore_default()
#         input_page.tap_menu()
#         input_page.tap_keyboard_mode()
#         input_page.to_which_keyboard_mode('普通键盘')
#         input_page.tap_menu()
#         input_page.tap_keyboard_layout()
#         list_num = input_page.get_list_total_num('//*[@resource-id="com.huawei.ohos.inputmethod:id/recycler_view'
#                                                  '"]/android.widget.LinearLayout')
#         for i in range(1, list_num):
#             text = input_page.find_element_by_xpath(
#                 '//*[@resource-id="com.huawei.ohos.inputmethod:id/recycler_view"]/android.widget.LinearLayout['
#                 '%d]/android.widget.TextView' % (
#                         1 + i)).get_attribute('text')
#             if text == 'Dvorak':
#                 golVar.set_value('language_layout', 'relative_layout_dvorak')
#             else:
#                 golVar.set_value('language_layout', 'relative_layout_en')
#             input_page.find_element_by_xpath_click('//*[@resource-id="com.huawei.ohos.inputmethod:id/recycler_view'
#                                                    '"]/android.widget.LinearLayout[%d]' % (1 + i))
#             time.sleep(1)
#             os.system('adb shell input tap 540 1800')
#             os.system('adb shell input tap 540 1800')
#             # 点击删除键
#             input_page.input_characters('delete', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             # 点击空格键
#             input_page.input_characters('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             os.system('adb shell input tap 540 1800')
#             # 点击回车键
#             input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                         screen_size_list[1])
#             input_page.tap_menu()
#             input_page.tap_keyboard_layout()
#         input_page.find_element_by_xpath_click(
#             '//*[@resource-id="com.huawei.ohos.inputmethod:id/recycler_view"]/android.widget.LinearLayout[1]')
#     # 收起键盘
#     input_page.menu_back()
#
#
# @allure.story('打点测试，遍历 30 种键盘')
# def test_31(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('单手模式')
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('悬浮键盘')
#     input_page.tap_menu()
#     input_page.tap_keyboard_mode()
#     input_page.to_which_keyboard_mode('拇指模式')
#     input_page.tap_menu()
# @allure.story('检查字符点击与上屏功能[一些符号上屏失败，需调研]')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0003(set_device_id_list, set_driver_pool, cmdopt):
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     # 关闭数字行
#
#     KeyboardSettingPage(set_driver_pool).to_page_setting_page().check_number_capitalization('noselect')
#     PageSettingPage(set_driver_pool).back_to_setting_page().back_to_input_page()
#     time.sleep(2)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     # 进入符号页面
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     time.sleep(2)
#     input_page.click_symbol_keyboard('中文')
#     input_page.click_symbol_keyboard('锁住')
#     # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
#     input_page.click_symbol_keyboard('\u3002')
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '，。？！、：；……“”‘’@～—＃＊｜（）'
#     # input_page.return_to_launcher(set_device_id_list[which_driver_pool])
#
#
# @allure.story('检查换行键功能')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0006(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         光标换行，有什么好的方法
#     '''
#     pass
#
#
# @allure.story('检查空格键功能使用')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0010(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_setting()
#     # 关闭数字行
#
#     KeyboardSettingPage(set_driver_pool).to_page_setting_page().check_number_capitalization('noselect')
#     PageSettingPage(set_driver_pool).back_to_setting_page().back_to_input_page()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     input_page.input_characters('nihao', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '你好'
#
#
# @allure.story('切换至符号页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0014(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     # 进入符号页面
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     time.sleep(2)
#     # 判断是否进入符号页面
#     input_page.is_element_exist('中文')
#     input_page.is_element_exist('\u3002')
#     input_page.click_symbol_keyboard('返回')
#     # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '去'
#
#
# @allure.story('逗号检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0053(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters(',', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.long_press(',', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '，！'
#
#
# @allure.story('空格检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0054(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         输入状态：目前自己实现的输入逻辑是在输入字母后，自动点击空格，是一个连贯的过程，所以单独的输入状态不好找
#     '''
#     pass
#
#
# @allure.story('句号检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_01_0055(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.input_characters('.', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     input_page.long_press('.', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '。？'
#
#
# @allure.story('切换至普通符号页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_02_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#
#     # 进入符号页面
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0], screen_size_list[1])
#     time.sleep(2)
#     # 判断是否进入符号页面
#     input_page.is_element_exist('中文')
#     input_page.is_element_exist('\u3002')
#     input_page.click_symbol_keyboard('返回')
#     # input_page.click_symbol_keyboard('，。？！、：；……“”‘’@～—＃＊｜（）')
#     input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('q', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     print(text)
#     assert text == '去'
#     # 还原至26键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#
#
# @allure.story('检查字符点击与上屏功能-英文键盘')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_03_0002(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         疑问细节：分别点击键盘中所有字母和阿拉伯数字键，点击数字键？
#     '''
#     pass
#
#
# @allure.story('检查符号点击与上屏功能-26键英文键盘')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_03_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'english':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_symbol')
#     input_page.input_characters('@#$%&-+()/:;!?_.', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('asterisk', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('single-quotation', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('quotation', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     golVar.set_value('language_layout', 'relative_layout_en')
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '@#$%&-+()/:;!?_.*\'\"\")'
#
#
# @allure.story('手写识别体验')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_04_0010(set_device_id_list, set_driver_pool, cmdopt):
#     '''
#         手写how to do？
#     '''
#     pass
#
#
# @allure.story('笔画检查')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_05_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为英文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     time.sleep(2)
#     input_page.input_characters('一丨丿丶ㄥ通配', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '权'
#
#
# @allure.story('检查26键【?123】功能键显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0001(set_device_id_list, set_driver_pool, cmdopt):
#     '''检查符号键样式'''
#     pass
#
#
# @allure.story('点击【123】功能键盘检查键盘显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0003(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     # 手写
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('手写键盘')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_handwriting = input_page.screenshot2('手写-num')
#     # 笔画
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('笔画')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_bihua = input_page.screenshot2('笔画-num')
#     # 9键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('9键')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_9key = input_page.screenshot2('9-num')
#     # 26键
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     time.sleep(3)
#     input_page.input_characters('num', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     pic_26key = input_page.screenshot2('26-num')
#     result1 = input_page.compare(pic_handwriting, pic_bihua)
#     result2 = input_page.compare(pic_bihua, pic_9key)
#     result3 = input_page.compare(pic_9key, pic_26key)
#     '''
#         截图比较
#     '''
#
#
# @allure.story('点击数字键盘任意按键检查字符上屏显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0009(set_device_id_list, set_driver_pool, cmdopt):
#     """
#         左侧符号控件的滑动点击
#     """
#
#
# @allure.story('检查符号页面分组显示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_06_0033(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     test_layout_list = ['手写键盘']  # , '笔画', '9键', '26键'
#     for layout in test_layout_list:
#         input_page.tap_menu()
#         input_page.tap_keyboard_layout()
#         input_page.to_which_keyboard_layout(layout)
#         input_page.input_characters('symbol', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         first_element_bounds_str = input_page.find_element_by_xpath('//*[@resource-id="com.huawei.ohos.inputmethod:id'
#                                                                     '/symbols_rcv"]/android.widget.LinearLayout['
#                                                                     '1]').get_attribute('bounds')
#         first_element_bounds = re.findall(r'\d+', first_element_bounds_str)
#         test_list = ['常用', '中文', '英文', '网络', '特殊', '数学', '序号', '日文', '希腊文', '藏文', '俄文', '拉丁文', '注音', '部首', '制表']
#         for i in test_list:
#             input_page.symbol_grouping_bar(i, 'left')
#             input_page.touch_tap((int(first_element_bounds[0]) + int(first_element_bounds[2])) / 2,
#                                  (int(first_element_bounds[1]) + int(first_element_bounds[3])) / 2)
#         input_page.click_symbol_keyboard('返回')
#
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '，，,@☆+①アαༀаÄā丨╭'
#     '''
#         流程能走通，但结果如何去检测？
#     '''
#
#
# @allure.story('点击语音输入键，语音输入')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_07_0036(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.voice_input('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                            screen_size_list[1])
#     os.system('say 你好')
#     time.sleep(3)
#     input_page.menu_back()
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     text = input_page.find_element_by_class("android.widget.EditText").text
#     assert text == '你好。'
#
#
# @allure.story('中文九键键盘下显示验证码')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_08_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#         短信验证码相关验证
#     '''
#
#
# @allure.story('不同APP显示短信验证码-01')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_08_0019(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     '''
#         短信验证码相关验证
#     '''
#
#
# @allure.story('剪贴板内容最多显示5条')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0007(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     # 检查键盘，非中文键盘，点击'切换'键，切换为中文键盘，检查完后点击enter清空文本框内容，再进行输入
#     if input_page.check_language(set_device_id_list[which_driver_pool], screen_size_list[0],
#                                  screen_size_list[1]) == 'chinese':
#         print('当前为英文键盘')
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     else:
#         input_page.input_characters('switch', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#         input_page.input_characters('enter', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                     screen_size_list[1])
#     input_page.input_characters('nihaozhelishibeijing', set_device_id_list[which_driver_pool], screen_size_list[0],
#                                 screen_size_list[1])
#     input_page.clean_text()
#     input_page.tap_menu()
#     input_page.tap_edit()
#     operation_list1 = ['句首', '选择', 'right', 'right', '复制']
#     for operate1 in operation_list1:
#         input_page.edit_operation(operate1)
#     operation_list2 = ['选择', 'right', 'right', '复制']
#     for operate2 in operation_list2:
#         input_page.edit_operation(operate2)
#     operation_list3 = ['选择', 'right', '复制']
#     for operate3 in operation_list3:
#         input_page.edit_operation(operate3)
#     operation_list4 = ['选择', 'right', 'right', '复制']
#     for operate4 in operation_list4:
#         input_page.edit_operation(operate4)
#     operation_list5 = ['全选', '复制']
#     for operate5 in operation_list5:
#         input_page.edit_operation(operate5)
#     input_page.menu_back()
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     num = input_page.get_clipboard_num()
#     assert num == '(5/5)'
#     assert not input_page.is_element_exist('使用剪贴板以轻松粘贴文本')
#
#
# @allure.story('点击剪贴板复制内容可上屏')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0009(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     input_page.paste_clipboard_item()
#
#
# @allure.story('点击删除键，此内容消失')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_09_0026(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     input_page.tap_clipboard()
#     str1 = input_page.delete_clipboard_item()
#     assert str1 == '(0/5)'
#
#
# @allure.story('使用外接键盘输入字符能够正常展示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_12_0005(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     '''
#         外接键盘
#     '''
#
#
# @allure.story('使用虚拟键盘输入字符能够正常展示')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_12_0006(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     '''
#         外接键盘
#     '''
#
#
# @allure.story('切换系统分辨率查看帐号登录状态')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_01_02_0032(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     time.sleep(1)
#     login_page.switch_wm_size(set_device_id_list[which_driver_pool], '800x1760')
#     time.sleep(1)
#     # 检验登录状态：1.非登录状态下，页面不存在'登录华为账号'关键字，页面底部没有'退出登录'按钮
#     # 检验细节：切换分辨率后，各控件点击后，响应是否正常
#     assert not login_page.is_element_exist('登录华为账号')
#     assert login_page.is_element_exist('退出登录')
#     theme_setting_page = login_page.my_skins()
#     time.sleep(1)
#     assert theme_setting_page.is_element_exist('皮肤')
#     theme_setting_page.back_to_previous_page()
#     font_setting_page = login_page.my_fonts()
#     time.sleep(1)
#     assert font_setting_page.is_element_exist('字体')
#     font_setting_page.back_to_previous_page()
#     sync_thesaurus_page = login_page.my_sync()
#     time.sleep(1)
#     assert sync_thesaurus_page.is_element_exist('同步词库')
#     sync_thesaurus_page.back_to_previous_page()
#     back_up_page = login_page.my_back_up()
#     time.sleep(1)
#     assert back_up_page.is_element_exist('备份设置项')
#     back_up_page.back_to_previous_page()
#     keyboard_setting_page = login_page.to_setting_page()
#     time.sleep(1)
#     assert keyboard_setting_page.is_element_exist('小艺输入法')
#     keyboard_setting_page.back_to_previous_page()
#     login_page.log_out('取消')
#     login_page.log_out('继续退出')
#     time.sleep(3)
#     assert login_page.is_element_exist('登录华为帐号')
#     # print('login_page:', login_page.driver.page_source)
#     login_page.log_in('取消')
#     login_page.switch_wm_size(set_device_id_list[which_driver_pool], 'reset')
#     time.sleep(3)
#     assert not login_page.is_element_exist('登录华为账号')
#     assert login_page.is_element_exist('退出登录')
#
#
# @allure.story('已登录帐号进入云备份设置页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_01_0004(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     time.sleep(1)
#     login_page.log_out('继续退出')
#     time.sleep(1)
#     login_page.log_in('取消')
#     time.sleep(1)
#     back_up_page = login_page.my_back_up()
#     time.sleep(1)
#     assert back_up_page.is_element_exist('备份设置项')
#     back_up_page.back_to_previous_page()
#
#
# @allure.story('已登录帐号进入云备份设置页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_01_0017(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     back_up_page = login_page.my_back_up()
#     back_up_page.restore_setting('确定')
#     back_up_page.back_to_previous_page()
#
#
# @allure.story('手动同步词库图标状态-同步完成01')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_02_02_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     input_page.tap_menu()
#     login_page = input_page.tap_login()
#     sync_thesaurus_page = login_page.my_sync()
#     time.sleep(1)
#     sync_thesaurus_page.sync_thesaurus()
#     current_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
#     print(current_time)
#     str_time = sync_thesaurus_page.get_sync_time()
#     print('str_time:', str_time)
#     assert current_time == str_time
#
#
# @allure.story('在语音输入页点击Menu进入菜单页')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     assert input_page.is_element_exist('键盘布局')
#     '''
#     # 切换至横屏
#     input_page.rotate_the_screen_to_horizontal()
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     '''
#
#
# @allure.story('使用普通话进行语音输入无异常')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0013(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     input_page.voice_change_language('普通话')
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     os.system('say 你好')
#     text = input_page.find_element_by_id('com.android.mms:id/embedded_text_editor').text
#     assert text == '你好。'
#
#
# @allure.story('使用粤语普通话免切换方言进行语音输入反馈无异常')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_01_0015(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0001']['textmessage'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     input_page.bring_up_sms_page()
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.clear_sms_data(set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#     input_page.tap_menu()
#     input_page.tap_keyboard_layout()
#     input_page.to_which_keyboard_layout('26键')
#     input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                           screen_size_list[1])
#     time.sleep(1)
#     input_page.voice_change_language('粤语')
#     if input_page.deal_sys_dialog('仅使用期间允许', '仅使用期间允许'):
#         time.sleep(1)
#         input_page.bring_up_sms_page()
#         time.sleep(1)
#         input_page.long_press('space', set_device_id_list[which_driver_pool], screen_size_list[0],
#                               screen_size_list[1])
#
#     os.system('say -v Sin-ji 你好')
#     text = input_page.find_element_by_id('com.android.mms:id/embedded_text_editor').text
#     assert text == '你好。'
#
#
# @allure.story('添加语言确定恢复默认设置，语言页无变化')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0017(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     language_setting_page = keyboard_setting_page.to_language_setting_page()
#     language_setting_page.add_language_list2('南非荷兰文', 'af')
#     setting_page = language_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     language_setting_page = setting_page.to_language_setting_page()
#     status = language_setting_page.check_the_language_states('南非荷兰文')
#     # 通过语言item勾选状态以此判断是否存在'添加语言'中
#     assert status == 'true'
#
#
# @allure.story('在普通模式改变皮肤确定恢复默认设置，恢复成默认皮肤')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0022(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     theme_setting_page = keyboard_setting_page.to_theme_setting_page()
#     theme_setting_page.switch_theme('默认')
#     theme_setting_page.switch_theme('墨绿色')
#     theme_setting_page.switch_theme('浅艾蓝')
#     theme_selected = theme_setting_page.search_selected_theme()
#     assert theme_selected == '浅艾蓝'
#     setting_page = theme_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     setting_page.to_theme_setting_page()
#     theme_selected2 = theme_setting_page.search_selected_theme()
#     assert theme_selected2 == '默认'
#
#
# @allure.story('非默认字体确定恢复默认设置，字体页无变化')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0026(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     font_setting_page = keyboard_setting_page.to_font_setting_page()
#     font_data_list = ['系统字体', '鸿蒙字体', 'MidoRound', 'Joker', 'AriaSlab']
#     font_setting_page.change_font(font_data_list)
#     font_selected = font_setting_page.search_selected_font()
#     assert font_selected == 'AriaSlab'
#     setting_page = font_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     setting_page.to_font_setting_page()
#     font_selected2 = font_setting_page.search_selected_font()
#     assert font_selected2 == 'AriaSlab'
#
#
# @allure.story('打开一个模糊拼音选项确定恢复默认设置，选项恢复成默认全部关闭')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0041(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     fuzzy_pinyin_test_list = ['z = zh', 'c = ch', 'k = g']
#     chinese_setting_page.fuzzy_pinyin(fuzzy_pinyin_test_list)
#     status1 = chinese_setting_page.get_fuzzy_pinyin_status('z = zh')
#     status2 = chinese_setting_page.get_fuzzy_pinyin_status('c = ch')
#     status3 = chinese_setting_page.get_fuzzy_pinyin_status('k = g')
#     assert status1 == 'true'
#     assert status2 == 'true'
#     assert status3 == 'true'
#     # 退出模糊拼音页面
#     chinese_setting_page.back_to_previous_page()
#     # 退出中文设置页面
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     status = chinese_setting_page2.get_all_fuzzy_pinyin_status()
#     print(type(status), status)
#     assert status[0] == 10
#
#
# @allure.story('关闭拼音云输入确定恢复默认设置，拼音云输入开关打开')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0045(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     chinese_setting_page.chinese_setting_about_input('拼音云输入', '关闭')
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     status = chinese_setting_page2.get_all_status_in_chinese_setting('拼音云输入')
#     assert status == '开启'
#
#
# @allure.story('选择非关闭双拼输入选项确定恢复默认设置，选项恢复成默认关闭')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0049(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     chinese_setting_page = input_setting_page.click_which_item('中文设置', 'none')
#     chinese_setting_page.shuangpin_input('智能ABC')
#     chinese_setting_page.back_to_previous_page()
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     chinese_setting_page2 = input_setting_page2.click_which_item('中文设置', 'none')
#     text = chinese_setting_page2.get_shuangpin_input_text()
#     assert text == '关闭'
#
#
# @allure.story('关闭启用表情符号预测确定恢复默认设置，启用表情符号预测开关打开')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_02_0065(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.tap_menu()
#     keyboard_setting_page = input_page.tap_setting()
#     input_setting_page = keyboard_setting_page.to_input_setting_page()
#     input_setting_page.click_which_item('启用表情符号预测', 'none')
#     setting_page = input_setting_page.back_to_setting_page()
#     setting_page.restore_to_default_settings('确定')
#     input_setting_page2 = setting_page.to_input_setting_page()
#     status = input_setting_page2.check_item_status('启用表情符号预测')
#     assert status == 'true'
#
#
# @allure.story('入口-设置')
# # 通过 case_number 在 case_id 表中查询，对应的 case 使用哪个 driver
# def test_InputMethod_SCB_Func_03_03_02_0001(set_device_id_list, set_driver_pool, cmdopt):
#     set_device_id_list = set_device_id_list
#     # pool 池中 driver 与 device_id 为一对一的关系
#     which_driver_pool = int(cmdopt)
#     input_page = InputPage(set_driver_pool)
#     screen_size_list.clear()
#     get_vm_size(set_device_id_list[which_driver_pool], screen_size_list)
#     os.system(test_adb_data['adb_01_01_01_0003']['emptyinput'] % set_device_id_list[which_driver_pool])
#     time.sleep(1)
#     os.system(test_adb_data['adb_01_01_01_0004']['upkeyboard'] % set_device_id_list[which_driver_pool])
#     time.sleep(3)
#     print('当前键盘：', golVar.get_value('language_layout'))
#     input_page.return_to_launcher(set_device_id_list[which_driver_pool])
#     input_page.find_element_by_xpath('//android.widget.TextView[@content-desc="小艺输入法"]').click()
#     login_page = LoginPage(set_driver_pool)
#     setting_page = login_page.to_setting_page()
#     page_setting_page = setting_page.to_page_setting_page()
#     change_font_size_page = page_setting_page.change_font_size()
#     assert change_font_size_page.is_element_exist('字体大小')






# if __name__ == '__main__':
#     golVar.__init__()
#     pytest.main()
