
from public.base_function import BaseFunction
from page.search_page import SearchPage

class HomePage(BaseFunction):

    def begin_home_page(self):
        # home_page = HomePage(self.driver)
        if self.is_element_exist('立即安装'):
            # 取消升级
            self.deal_update_bullet_frame('com.cto51.student:id/update_cancel')
            if not self.is_element_exist('首页'):
                # 关闭广告弹框
                self.deal_ad_bullet_frame('com.cto51.student:id/iv_close')

    def to_search_page(self):
        self.find_element_by_xpath_click('//*[@resource-id="com.cto51.student:id/et_search"]')
        return SearchPage(self.driver)
