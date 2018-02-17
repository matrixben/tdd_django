from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # Jason听说有一个很酷的在线待办事项应用
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def testWhenOpenWebsiteThenShowTodolists(self):
        # 他去看了这个应用的首页
        self.browser.get(self.live_server_url) #'http://localhost:8000'

        # 他注意到网页的标题和头部都包含"To-Do"这个词
        self.assertIn('To-Do', self.browser.title)
        html_head = self.browser.find_element_by_tag_name("h1")
        self.assertIn('To-Do', html_head.text)

        # 应用邀请他输入一个待办事项
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(input_box.get_attribute('placeholder'), 'Please enter your to-do item.')
        # 他在一个文本框中输入"learn django in a month"
        input_text = "learn django in a month"
        input_box.send_keys(input_text)
        # 他按回车键后,页面更新了
        input_box.send_keys(Keys.ENTER)
        # 待办事项表格中显示了"1.learn django in a month"
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        # self.assertTrue(any(row.text == input_text for row in rows),
        #                "New item did not appear in the table")
        self.assertIn("1. " + input_text, [row.text for row in rows])
        # 输入回车后转到新url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+') # 检查字符串是否匹配正则表达式
        # 页面中又显示了一个文本框,可以输入其他的待办事项
        input_box = self.browser.find_element_by_id("id_new_item")
        # 他输入了"write a new virtual currency base on open source coin"
        input_text2 = "write a new virtual currency base on open source coin"
        input_box.send_keys(input_text2)
        input_box.send_keys(Keys.ENTER)
        # 待办事项表格中显示了之前输入的两个待办事项
        self.check_for_row_in_list_table("1. "+input_text)
        self.check_for_row_in_list_table("2. "+input_text2)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

"""
if __name__ == '__main__':
    unittest.main()

阅读Django官方教程，以巩固知识
"""
