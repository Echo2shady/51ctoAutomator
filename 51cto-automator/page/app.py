import multiprocessing
import os

from appium import webdriver

from lib.loggers import log
from page.main_page import MainPage


class App:

    def start(self, port, device, sysPort):
        caps = {'platformName': 'Android', 'platformVersion': '8.1', 'deviceName': 'nexus 6p',
                'newCommandTimeout': 2000,
                'appPackage': 'com.huawei.ohos.inputmethod',
                'appActivity': 'com.appstore.view.activity.PrimaryActivity',
                'systemPort': sysPort,
                'id': device}

        self.driver = webdriver.Remote('http://localhost:'+str(port)+'/wd/hub', caps)
        # self.update_settings({"normalizeTagNames": True})
        self.driver.implicitly_wait(5)
        log.info('start-driver').debug(self.driver)
        # driver_list[] =
        return MainPage(self.driver)

    def quit(self):
        self.driver.quit()

