import time

from page.home_page import HomePage
from public.base_function import BaseFunction


class LoginPage(BaseFunction):
    # 密码登录

    def pass_word_login(self, device, account, password):
        # 账号输入框
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/tv_login_by_pwd"]')
        self.driver.implicitly_wait(15)
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/tv_account"]')
        # self.find_element_by_xpath_click('//*[@text="密码登录"]')
        time.sleep(3)
        self.input_text(device, account)
        # 收起智能提示框
        # time.sleep(5)
        # self.find_element_by_xpath_click('//*[@text="密码登录"]')
        # 密码输入框
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/tv_pwd"]')
        # self.find_element_by_xpath_click('//*[@text="密码登录"]')
        time.sleep(3)
        self.input_text(device, password)
        time.sleep(3)
        self.back_to_previous_page()
        # 收起智能提示框
        # self.find_element_by_xpath_click('//*[@text="密码登录"]')
        # 选中同意协议选项
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/cb_licence"]')
        # self.find_element_by_xpath_click('//*[@text="密码登录"]')
        # 获取控件属性，是否为选中状态
        if self.get_control_status('com.cto51.student:id/cb_licence', 'checked') == 'true':
            self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/btn_login"]')
            return HomePage(self.driver)
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/btn_login"]')
        # print('lalala:', self.get_control_status('com.cto51.student:id/cb_licence', 'checked'))
