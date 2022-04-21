from public.base_function import BaseFunction


class SearchPage(BaseFunction):
    def search_class(self):
        self.driver.find_element_by_xpath('//*[@resource-id="com.cto51.student:id/toolbar_search_cancel_tv"]').click()
