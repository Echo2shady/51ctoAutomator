import json
import math
import operator
import os
import re
import time
from functools import reduce

import numpy
from PIL import ImageChops
from PIL.Image import Image, new
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

import golVar

import time
import os
from PIL import ImageFile
from PIL import Image
import math
import operator

from lib.get_path import get_path_data, get_path

ImageFile.LOAD_TRUNCATED_IMAGES = True
PATH = lambda p: os.path.abspath(p)

test_case_data = get_path_data('/data/case_data.yml')
test_adb_data = get_path_data('/data/adb_data.yml')


class BaseFunction:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        print(driver)

    # 判断元素是否存在
    def is_element_exist(self, element):
        source = self.driver.page_source
        if element in source:
            return True
        else:
            return False

    # 寻找元素集
    def find_elements(self, locator):
        try:
            return self.driver.find_elements(*locator)
        except:
            # self.handle_exception('find_elements')
            pass

    # 寻找元素
    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except:
            pass

    # 通过滑动的方式寻找text
    # def move_to_find_text(self, text):
    #     self.driver.find_element_by_android_uiautomator(
    #         'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector()'
    #         '.text("%s").instance(0))' % text)

    # 定位到元素后，进行点击操作
    def find_element_click(self, locator):
        try:
            self.find_element(locator).click()
        except:
            # self.handle_exception('find_element_click')
            pass

    # 通过text定位元素
    def find_element_by_text(self, text):
        try:
            return self.driver.find_element_by_android_uiautomator('new UiSelector().text("%s")' % text)

        except:
            pass
            # self.handle_exception('find_element_by_text')

    # 通过text定位元素并点击
    def find_element_by_text_click(self, text):
        try:
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("%s")' % text).click()
        except:
            pass
            # self.handle_exception('find_element_by_text_click')

    # 通过contenet-des定位元素
    def find_element_by_contenet_des(self, contenet):
        try:
            return self.driver.find_element_by_android_uiautomator('new UiSelector().description("%s")' % contenet)
        except:
            pass
            # self.handle_exception('find_element_by_contenet')

    # 通过contenet-des定位元素并点击
    def find_element_by_contenet_des_click(self, contenet):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiSelector().description("%s")' % contenet).click()
        except:
            pass
            # self.handle_exception('find_element_by_contenet_click')

    # 通过className定位元素
    def find_element_by_class(self, class_name):
        try:
            return self.driver.find_element_by_class_name(class_name)
        except:
            pass
            # self.handle_exception('find_element_by_class')

    # 通过className定位元素并点击
    def find_element_by_class_click(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name).click()
        except:
            pass
            # self.handle_exception('find_element_by_class_click')

    # 通过 id 寻找元素
    def find_element_by_id(self, id_name):
        try:
            return self.driver.find_element_by_id(id_name)
        except:
            pass
            # self.handle_exception('find_element_by_id')

    # 通过 id 寻找元素并点击
    def find_element_by_id_click(self, id_name):
        try:
            self.driver.find_element_by_id(id_name).click()
        except:
            pass
            # self.handle_exception('find_element_by_id_click')

    # 通过 xpath 寻找元素
    def find_element_by_xpath(self, xpath_name):
        try:
            return self.driver.find_element_by_xpath(xpath_name)
        except:
            pass
            # self.handle_exception('find_element_by_xpath')

    # 通过 xpath 寻找元素并点击
    def find_element_by_xpath_click(self, xpath_name):
        try:
            self.driver.find_element_by_xpath(xpath_name).click()
        except:
            pass
            # self.handle_exception('find_element_by_xpath_click')

    _gdpr_agree_button = (By.ID, 'com.huawei.ohos.inputmethod:id/btn_ok')
    _gdpr_disagree_button = (By.ID, 'com.huawei.ohos.inputmethod:id/btn_deny')
    _gdpr_learn_more_button = (By.ID, 'com.huawei.ohos.inputmethod:id/tv_content2')

    # 点击键盘按键
    def click_keys(self, words, keys_list, device_id, screen_size_width, screen_size_height):
        """
        :param words: 需要输入的按键
        :param keys_list: 按键的坐标信息
        :param device_id: 设备 device id
        :param screen_size_width: 屏幕分辨率宽
        :param screen_size_height: 屏幕分辨率高
        :return:
        """
        for key_info in keys_list:
            if words == key_info['code']:
                os.system(test_adb_data['adb_01_01_01_0006']['shortclick'] % (
                    device_id, str(float(key_info['x']) * float(screen_size_width)),
                    str(float(key_info['y']) * float(screen_size_height))))
                print(str(float(key_info['x']) * float(screen_size_width)),
                      str(float(key_info['y']) * float(screen_size_height)))

    # 输入字符
    def input_characters(self, words, device_id, screen_size_width, screen_size_height):
        """
        :param words: 输入的字符
        :param device_id: 设备 device id
        :param screen_size_width: 屏幕分辨率宽
        :param screen_size_height: 屏幕分辨率高
        :return:
        """
        if len(words) != 0:
            language_layout = golVar.get_value('language_layout')
            print('language_layout:', language_layout)
            relative_layout_data_path = get_path('/layout/%s' % language_layout)
            with open(relative_layout_data_path) as file:
                keys_data = json.loads(file.read())
                keys_list = keys_data['keys']
                print(keys_list, type(keys_list))
            if (words == 'space') | (words == 'symbol') | (words == 'quotation') | (words == 'single-quotation') | \
                    (words == 'asterisk') | (words == 'enter') | (words == 'delete') | (words == 'shift') | \
                    (words == 'switch') | (words == 'emjo') | (words == 'num') | (words == '通配') | (words == '分词'):
                self.click_keys(words, keys_list, device_id, screen_size_width, screen_size_height)
            # 字母
            elif re.search(r'\W', words) is None:
                new_words = words.replace('通配', '0').replace('分词', '1')
                for i in new_words:
                    time.sleep(0.3)
                    print('点击字符：', i)
                    if golVar.get_value('language_layout') == '笔画':
                        if i == '0':
                            self.click_keys('通配', keys_list, device_id, screen_size_width, screen_size_height)
                        elif i == '1':
                            self.click_keys('分词', keys_list, device_id, screen_size_width, screen_size_height)
                        else:
                            self.click_keys(i, keys_list, device_id, screen_size_width, screen_size_height)
                    else:
                        self.click_keys(i, keys_list, device_id, screen_size_width, screen_size_height)
                time.sleep(1)
                self.click_keys('space', keys_list, device_id, screen_size_width, screen_size_height)
            # 符号
            else:
                for i in words:
                    self.click_keys(i, keys_list, device_id, screen_size_width, screen_size_height)
                time.sleep(1)

    """
    # 点击候选词
    def click_candidate(self, click_actions, device_id, screen_size_width, screen_size_height):
        candidate_data_path = get_path('/layout/candidate_layout')
        with open(candidate_data_path) as file:
            candidate_coordinate_data = json.loads(file.read())
            candidate_coordinate_list = candidate_coordinate_data['keys']
            for candidate in candidate_coordinate_list:
                if click_actions == candidate['code']:
                    os.system(
                        test_adb_data['adb_01_01_01_0006']['shortclick'] %
                        (device_id, str(float(candidate['x']) * float(screen_size_width))
                         , str(float(candidate['y']) * float(screen_size_height))))
                    print(candidate['x'] * screen_size_width
                          , candidate['y'] * screen_size_height)
    
    # 通过坐标的方式点击menu中的功能按键
    def click_keyboard_menu(self, menu, device_id, screen_size_width, screen_size_height):
        relative_layout_data_path = get_path('/layout/menu_layout')
        with open(relative_layout_data_path) as file:
            menu_location_data = json.loads(file.read())
            menu_location = menu_location_data['key']
            for i in menu_location:
                if menu == 'Layout':
                    os.system(test_adb_data['adb_01_01_01_0006']['shortclick'] %
                              (device_id, str(float(i['x']) * float(screen_size_width))
                               , str(float(i['y']) * float(screen_size_height))))
    """

    # 中英检查
    def check_language(self, device_id, screen_size_width, screen_size_height):
        """
        :param device_id: 设备 device id
        :param screen_size_width: 屏幕分辨率宽
        :param screen_size_height: 屏幕分辨率高
        :return:
        """
        words = 'q'
        self.input_characters(words, device_id, screen_size_width, screen_size_height)
        time.sleep(2)
        if self.find_element_by_class("android.widget.EditText").text == 'q ':
            return 'english'
        else:
            return 'chinese'

    # 回到手机桌面
    def return_to_launcher(self, device_id):
        """
        :param device_id: 设备 device id
        :return:
        """
        os.system(test_adb_data['adb_01_01_01_0015']['home'] % device_id)

    # 清空已有内容
    def editClear(self, text1):
        # 123代表光标移动到末尾
        self.driver.keyevent(123)
        for z in range(0, len(text1)):
            # 67退格键
            self.driver.keyevent(67)

    # 调起系统短信页面
    def bring_up_sms_page(self):
        self.driver.implicitly_wait(10)
        self.find_element_by_id('com.android.mms:id/embedded_text_editor').click()

    # 清空系统短信输入框内容
    def clear_sms_data(self, device_id, screensize_width, screensize_height):
        """
        :param device_id: 设备 device id
        :param screensize_width: 屏幕分辨率宽
        :param screensize_height: 屏幕分辨率高
        :return:
        """
        status = True
        while status:
            text = self.find_element_by_id('com.android.mms:id/embedded_text_editor').text
            if text == '短信/彩信':
                print('短信内容清空')
                status = False
            else:
                self.long_press('delete', device_id, screensize_width, screensize_height)

    # 长按按键
    def long_click_keys(self, words, keys_list, device_id, screen_size_width, screen_size_height):
        """
        :param words: 输入需要长按的字符
        :param keys_list: 按键坐标数据
        :param device_id: 设备 device id
        :param screen_size_width: 屏幕分辨率宽
        :param screen_size_height: 屏幕分辨率高
        :return:
        """
        for key_info in keys_list:
            if words == key_info['code']:
                print(key_info['x'], key_info['y'])
                os.system(test_adb_data['adb_01_01_01_0007']['longclick'] %
                          (device_id, str(float(key_info['x']) * float(screen_size_width)),
                           str(float(key_info['y']) * float(screen_size_height)),
                           str(float(key_info['x']) * float(screen_size_width)),
                           str(float(key_info['y']) * float(screen_size_height))))

                print(str(float(key_info['x']) * float(screen_size_width)),
                      str(float(key_info['y']) * float(screen_size_height))
                      , str(float(key_info['x']) * float(screen_size_width)),
                      str(float(key_info['y']) * float(screen_size_height)))

    # 键盘按键长按操作
    def long_press(self, words, device_id, screen_size_width, screen_size_height):
        """
        :param words: 输入需要长按的字符
        :param device_id: 设备 device id
        :param screen_size_width: 屏幕分辨率宽
        :param screen_size_height: 屏幕分辨率高
        :return:
        """
        if len(words) != 0:
            language_layout = golVar.get_value('language_layout')
            print('language_layout:', language_layout)
            relative_layout_data_path = get_path('/layout/%s' % language_layout)
            with open(relative_layout_data_path) as file:
                keys_data = json.loads(file.read())
                keys_list = keys_data['keys']
                print(keys_list, type(keys_list))
            if (words == 'space') | (words == 'symbol') | (words == 'quotation') | (words == 'enter') | (
                    words == 'delete') | (words == 'shift') | (words == 'switch') | (words == 'emjo'):
                self.long_click_keys(words, keys_list, device_id, screen_size_width, screen_size_height)
            # elif words == ',':
            #     self.long_click_keys('symbol', keys_list, device_id, screen_size_width, screen_size_height)
            #     self.long_click_keys(words, keys_list, device_id, screen_size_width, screen_size_height)
            #     self.long_click_keys('symbol', keys_list, device_id, screen_size_width, screen_size_height)
            elif words == '.':
                self.long_click_keys(words, keys_list, device_id, screen_size_width, screen_size_height)
            else:
                for i in words:
                    self.long_click_keys(i, keys_list, device_id, screen_size_width, screen_size_height)
                time.sleep(1)
                # self.click_keys('space', keys_list, device_id, screen_size_width, screen_size_height)

    # tap封装
    def touch_tap(self, x, y, duration=100):  # 点击坐标  ,x1,x2,y1,y2,duration
        '''
        method explain:点击坐标
        parameter explain：【x,y】坐标值,【duration】:给的值决定了点击的速度
        Usage:
            device.touch_coordinate(277,431)      #277.431为点击某个元素的x与y值
        '''
        # screen_width = self.driver.get_window_size()['width']  # 获取当前屏幕的宽
        # screen_height = self.driver.get_window_size()['height']  # 获取当前屏幕的高
        # a = (float(x) / screen_width) * screen_width
        # x1 = int(a)
        # b = (float(y) / screen_height) * screen_height
        # y1 = int(b)
        # self.driver.tap([(x1, y1), (x1, y1)], duration)
        self.driver.tap([(x, y), (x, y)], duration)

    # 截图对比
    def screenshot(self, name):
        """
        :param name: 截图命名
        :return: 返回当前截图文件绝对路径
        """
        path = PATH(os.getcwd() + "/TestResult")
        if not os.path.isdir(PATH(os.getcwd() + "/TestResult")):
            os.makedirs(path)
        os.popen("adb wait-for-device")
        time.sleep(1)  # 由于多次出现截图延迟现象（每次截图都截的是上次操作的画面），故此处设置一个等待
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + name + '_tmp.png'))
        # os.popen("adb pull /data/local/tmp/tmp1.png " + PATH('/Users/xm210407/PycharmProjects/Kika/testcase/'))
        time.sleep(1)
        os.popen("adb shell rm /data/local/tmp/tmp.png")
        time.sleep(1)
        im = Image.open(PATH(path + "/" + name + '_tmp.png'))
        cropedIm = im.crop((0, 1020, 1079, 2200))
        cropedIm.save(PATH(path + "/" + name + '_tmp.png'))
        return PATH(path + "/" + name + '_tmp.png')

    # 截图对比
    def screenshot2(self, name):
        """
        :param name: 截图命名
        :return: 返回当前截图文件（截取 keyboard 的 mainView）绝对路径
        """
        path = PATH(os.getcwd() + "/TestResult")
        if not os.path.isdir(PATH(os.getcwd() + "/TestResult")):
            os.makedirs(path)
        os.popen("adb wait-for-device")
        time.sleep(1)  # 由于多次出现截图延迟现象（每次截图都截的是上次操作的画面），故此处设置一个等待
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + name + '_tmp.png'))
        time.sleep(1)
        os.popen("adb shell rm /data/local/tmp/tmp.png")
        time.sleep(1)
        im = Image.open(PATH(path + "/" + name + '_tmp.png'))
        if self.is_element_exist('resource-id="com.huawei.ohos.inputmethod:id/scale_view'):
            crop_bounds = self.container_bounds('scale_view', 'resource_id')
        else:
            crop_bounds = self.container_bounds('keyboard_main_view', 'resource_id')
        cropedIm = im.crop((crop_bounds[0], crop_bounds[1], crop_bounds[2], crop_bounds[3]))
        cropedIm.save(PATH(path + "/" + name + '_tmp.png'))
        return PATH(path + "/" + name + '_tmp.png')

    def screenshot_urlboard(self, name):
        """
        :param name: 截图命名
        :return: 返回当前截图文件（截取 keyboard 的 url 栏）绝对路径
        """
        path = PATH(os.getcwd() + "/TestResult")
        if not os.path.isdir(PATH(os.getcwd() + "/TestResult")):
            os.makedirs(path)
        os.popen("adb wait-for-device")
        time.sleep(1)  # 由于多次出现截图延迟现象（每次截图都截的是上次操作的画面），故此处设置一个等待
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + name + '_tmp.png'))
        time.sleep(1)
        os.popen("adb shell rm /data/local/tmp/tmp.png")
        time.sleep(1)
        im = Image.open(PATH(path + "/" + name + '_tmp.png'))
        crop_bounds = self.container_bounds('extra_container_top', 'resource_id')
        cropedIm = im.crop((crop_bounds[0], crop_bounds[1], crop_bounds[2], crop_bounds[3]))
        cropedIm.save(PATH(path + "/" + name + '_tmp.png'))
        return PATH(path + "/" + name + '_tmp.png')

    def screenshot_universal(self, name, index):
        """
        :param name: 截图名称
        :param index: 非中英键盘 layout 中，需要截取的 layout 下标
        :return: 返回当前截图文件（截取 layout 图标）绝对路径
        """
        path = PATH(os.getcwd() + "/TestResult")
        if not os.path.isdir(PATH(os.getcwd() + "/TestResult")):
            os.makedirs(path)
        os.popen("adb wait-for-device")
        time.sleep(1)  # 由于多次出现截图延迟现象（每次截图都截的是上次操作的画面），故此处设置一个等待
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(1)
        os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + name + '_tmp.png'))
        time.sleep(1)
        os.popen("adb shell rm /data/local/tmp/tmp.png")
        time.sleep(1)
        im = Image.open(PATH(path + "/" + name + '_tmp.png'))
        crop_bounds = self.container_bounds(
            '//*[@resource-id="com.huawei.ohos.inputmethod:id/recycler_view"]/android.widget.FrameLayout[%d]'
            % index, 'xpath')
        cropedIm = im.crop((crop_bounds[0], crop_bounds[1], crop_bounds[2], crop_bounds[3]))
        cropedIm.save(PATH(path + "/" + name + '_tmp.png'))
        return PATH(path + "/" + name + '_tmp.png')

    def compare(self, pic1, pic2):
        '''
        :param pic1: 图片1路径
        :param pic2: 图片2路径
        :return: 返回对比的结果
        '''
        image1 = Image.open(pic1)
        image2 = Image.open(pic2)
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        differ = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))
        print(differ)
        if differ < 2:
            print("应用成功")
        else:
            print("应用失败")
        return differ

    '''
    def compare2(self, image, target):
        
        :param pic1: 图片1路径
        :param pic2: 图片2路径
        :return: 返回对比的结果
        
        image = r'c:\temp\1.jpg'
        # target = r'c:\temp\2.jd03a4b21edd545812af46e7f84cc.jpg'
        target = r'c:\temp\Download-HD-Bamboo-Wallpapers.jpg'
        # target = r'c:\temp\Free-HD-Bamboo-Wallpapers-Download.jpg'
        img_gray = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
        tImg = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        h, w = tImg.shape[:2]
        h0 = h // 4
        h1 = h - h // 4
        w0 = w // 4
        w1 = w - w // 4
        template = tImg[h0:h1, w0:w1]
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = numpy.where(res >= threshold)
        print(loc)
        if len(loc[0]):
            print("True")
        else:
            print("False")
    '''

    # 滑动方法
    def swipeUp(self, driver, t=500, n=1):
        '''向上滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.75  # 起始y坐标
        y2 = l['height'] * 0.25  # 终点y坐标
        for i in range(n):
            driver.swipe(x1, y1, x1, y2, t)

    def swipeDown(self, driver, t=500, n=1):
        '''向下滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.5  # x坐标
        y1 = l['height'] * 0.25  # 起始y坐标
        y2 = l['height'] * 0.75  # 终点y坐标
        for i in range(n):
            driver.swipe(x1, y1, x1, y2, t)

    def swipLeft(self, driver, t=500, n=1):
        '''向左滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.75
        y1 = l['height'] * 0.8
        x2 = l['width'] * 0.25
        for i in range(n):
            driver.swipe(x1, y1, x2, y1, t)

    def swipRight(self, driver, t=500, n=1):
        '''向右滑动屏幕'''
        l = self.driver.get_window_size()
        x1 = l['width'] * 0.25
        y1 = l['height'] * 0.5
        x2 = l['width'] * 0.75
        for i in range(n):
            driver.swipe(x1, y1, x2, y1, t)

    # 获取控件坐标
    def container_bounds(self, resource, which_type):
        """
        :param resource: 控件resource-id（id/后面部分）
        :param which_type: 通过哪种方式定位：resource_id / xpath
        :return: 返回选中控件的坐标值，左上角坐标，右下角坐标
        """
        if which_type == 'resource_id':
            locate_container_bounds = self.find_element_by_xpath(
                '//*[@resource-id="com.huawei.ohos.inputmethod:id/%s"]' % resource).get_attribute('bounds')
        if which_type == 'xpath':
            locate_container_bounds = self.driver.find_element_by_xpath(resource).get_attribute(
                'bounds')
        container_bounds_string_to_array = re.findall(r'\d+', locate_container_bounds)
        container_sx, container_sy, container_ex, container_ey = float(container_bounds_string_to_array[0]), \
                                                                 float(container_bounds_string_to_array[1]), \
                                                                 float(container_bounds_string_to_array[2]), \
                                                                 float(container_bounds_string_to_array[3])
        return container_sx, container_sy, container_ex, container_ey

    # 返回上一个页面
    def back_to_previous_page(self):
        self.driver.back()

    # 华为手机系统选择语言页面，点击选中的语言，即可切换系统语言
    def to_system_language_picker(self, option, language):
        """
        :param option: 系统切换语言页面
        :param language: 打算切换的语言
        :return:
        """
        self.find_element_by_xpath_click('//*[@text="%s"]' % option)
        time.sleep(3)
        if self.is_element_exist(language):
            self.find_element_by_xpath_click('//*[@text="%s"]' % language)
        else:
            self.find_element_by_xpath_click('//*[@text="%s"]' % '添加语言')

    # 该方法暂不使用。原因：测试发现华为系列手机，点击系统语言列表中的语言item就可以切换至该语言
    def pick_which_sys_language(self, language):
        language_list_bounds = self.find_element_by_xpath(
            '//*[@resource-id="com.android.settings:id/main_content"]').get_attribute('bounds')
        container_bounds_string_to_array = re.findall(r'\d+', language_list_bounds)
        container_sx, container_sy, container_ex, container_ey = float(container_bounds_string_to_array[0]), \
                                                                 float(container_bounds_string_to_array[1]), \
                                                                 float(container_bounds_string_to_array[2]), \
                                                                 float(container_bounds_string_to_array[3])
        language_item = self.find_element_by_xpath('//*[@text="%s"]/preceding-sibling::android.widget.ImageView'
                                                   % language).get_attribute('bounds')
        item_bounds_string_to_array = re.findall(r'\d+', language_item)
        container_sx, container_sy, container_ex, container_ey = float(item_bounds_string_to_array[0]), \
                                                                 float(item_bounds_string_to_array[1]), \
                                                                 float(item_bounds_string_to_array[2]), \
                                                                 float(item_bounds_string_to_array[3])

        self.driver.swipe((container_sx + container_ex) / 2, (container_sy + container_ey) / 2,
                          (container_sx + container_ex) / 2, container_sy)

    # 通过xpath的方式定位控件，并获取指定元素下的元素个数
    def get_list_total_num(self, xpath_name):
        """
        :param xpath_name: list 控件的 xpath
        :return: 返回指定 list 中元素 item 的个数
        """
        list_item = self.driver.find_elements_by_xpath(xpath_name)
        print('list_item:', len(list_item))
        return len(list_item)

    def get_index(self, xpath_name, text):
        list_item = self.driver.find_elements_by_xpath(xpath_name)
        count = 0

    # '//*[@text="小艺输入法"]/../../following-sibling::android.widget'
    #                                                  '.ScrollView/androidx.appcompat.widget.LinearLayoutCompat'
    # 滑动控件的方式寻找元素并点击
    def scroll_to_find(self, list_xpath, which_one):
        """
        :param list_xpath: 该元素所在的list的xpath
        :param which_one: 想要找到的元素
        :return:
        """
        item_list_bounds = self.container_bounds(list_xpath, 'xpath')
        continue_swipe = True
        while continue_swipe:
            try:
                self.driver.find_element_by_xpath('//*[@text="%s"]' % which_one).click()
                continue_swipe = False
            except:
                before_swipe = self.driver.page_source
                self.driver.swipe((item_list_bounds[0] + item_list_bounds[2]) / 2,
                                  (item_list_bounds[3] - 1),
                                  (item_list_bounds[0] + item_list_bounds[2]) / 2,
                                  (item_list_bounds[1] + item_list_bounds[3]) / 2)
                after_swipe = self.driver.page_source
                if after_swipe == before_swipe:
                    continue_swipe = False

    # menu 菜单页面中，通过滑动的方式寻找指定元素
    def scroll_to_find_menu(self, id_name, which_one):
        """
        :param id_name: 菜单栏中元素id
        :param which_one: 菜单栏中元素的text属性
        :return:
        """
        item_list_bounds = self.container_bounds(id_name, 'resource_id')
        print('item_list_bounds:', item_list_bounds)
        status = True
        while status:
            self.driver.swipe((item_list_bounds[0] + item_list_bounds[2]) / 2,
                              (item_list_bounds[3] - 1),
                              (item_list_bounds[0] + item_list_bounds[2]) / 2,
                              (item_list_bounds[1] + 1))
            if self.driver.find_element_by_xpath('//*[@text="%s"]' % which_one).get_attribute('displayed') == 'true':
                status = False
                self.driver.find_element_by_xpath('//*[@text="%s"]' % which_one).click()

    # 系统设置页面中，寻找指定的元素
    def scroll_syspage_to_find(self, list_xpath, which_one):
        """
        :param list_xpath:元素所在的 list 的 xpath 路径
        :param which_one:元素的text属性
        :return:
        """
        item_list_bounds = self.container_bounds(list_xpath, 'xpath')
        continue_swipe = True
        while continue_swipe:
            try:
                self.driver.find_element_by_xpath('//*[@text="%s"]' % which_one).click()
                continue_swipe = False
            except:
                before_swipe = self.driver.page_source
                self.driver.swipe((item_list_bounds[0] + item_list_bounds[2]) / 2,
                                  (item_list_bounds[3] - 1),
                                  (item_list_bounds[0] + item_list_bounds[2]) / 2,
                                  (item_list_bounds[1] + item_list_bounds[3]) / 2)
                after_swipe = self.driver.page_source
                if after_swipe == before_swipe:
                    continue_swipe = False

    # 点击不同浏览器搜索框
    def click_browser_search_box(self, browser_type):
        if browser_type == 'MicroSoft':
            self.driver.find_element_by_xpath('//*[@resource-id="%s"]' % 'com.microsoft.emmx:id/search_box_text') \
                .click()
        if browser_type == 'Via':
            self.driver.find_element_by_xpath('//*[@resource-id="%s"]' % 'search_input').click()
        if browser_type == 'FireFox':
            self.driver.find_element_by_xpath('//*[@text="%s"]' % '搜索或输入网址').click()
        if browser_type == 'Chrome':
            self.driver.find_element_by_xpath('//*[@resource-id="%s"]' % 'com.android.chrome:id/search_box_text') \
                .click()
        if browser_type == 'Opera':
            self.driver.find_element_by_xpath('//*[@text="%s"]' % '搜索或输入网址').click()

    # 寻找不同浏览器中搜索框的文案
    def find_url_text(self, browser_type):
        if browser_type == 'MicroSoft':
            text = self.driver \
                .find_element_by_xpath('//*[@resource-id="%s"]' % 'com.microsoft.emmx:id/url_bar') \
                .get_attribute('text')
        if browser_type == 'Via':
            text = self.driver.find_element_by_xpath('//*[@resource-id="%s"]' % 'search_input').get_attribute('text')
        if browser_type == 'FireFox':
            text = self.driver.find_element_by_xpath('//*[@resource-id="%s"]' %
                                                     'org.mozilla.firefox:id/mozac_browser_toolbar_edit_url_view') \
                .get_attribute('text')
        if browser_type == 'Chrome':
            text = self.driver \
                .find_element_by_xpath('//*[@resource-id="%s"]' % 'com.android.chrome:id/url_bar') \
                .get_attribute('text')
        if browser_type == 'Opera':
            text = self.driver.find_element_by_xpath('//*[@resource-id="%s"]' %
                                                     'com.opera.browser:id/url_field').get_attribute('text')
        return text

    # 改变手机分辨率
    def switch_wm_size(self, device, vm_size):
        """
        :param device: device_id
        :param vm_size: 分辨率：800x1760，1200x2640，reset
        :return:
        """
        os.system('adb -s %s shell wm size %s' % (device, vm_size))

    # 旋转屏幕至横屏
    def rotate_the_screen_to_horizontal(self):
        self.driver.orientation = "LANDSCAPE"

    # 旋转屏幕至竖屏
    def rotate_the_screen_to_portrait(self):
        self.driver.orientation = "PORTRAIT"

    # 获取当前屏幕横竖屏状态
    def get_screen_orientation(self):
        return self.driver.orientation

    # 屏幕设置横竖屏
    def set_screen_orientation(self, orientation_setting):
        """
        :param orientation_setting: '横屏'、'竖屏'
        :return:
        """
        if orientation_setting == '横屏':
            self.driver.orientation = "LANDSCAPE"
        elif orientation_setting == '竖屏':
            self.driver.orientation = "PORTRAIT"

    # 文本框输入内容
    def input_text(self, device, text):
        os.popen('adb -s %s shell input text %s' % (device, text))
        print('00000:', 'adb -s %s shell input text %s' % (device, text))

    # 获取控件选中状态
    def get_control_status(self, name, attribute):
        self.find_element_by_xpath('//*[@resource-id="%s"]' % name).get_attribute(attribute)

    # 判断隐私协议弹框是否存在
    def check_privacy_policy(self):
        if self.is_element_exist('服务条款和隐私协议'):
            self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/tv_agree"]')

    # 处理升级弹框
    def deal_update_bullet_frame(self, method):
        """
        @param method: 立即安装：com.cto51.student:id/update_ok；知道了：com.cto51.student:id/update_cancel
        """
        self.find_element_by_xpath_click('//*[@resource-id="%s"]' % method)

    def deal_ad_bullet_frame(self, method):
        """
        @param method: 进入广告：com.cto51.student:id/iv_ad；关闭：com.cto51.student:id/iv_close
        """
        self.find_element_by_xpath_click('//*[@resource-id="%s"]' % method)

