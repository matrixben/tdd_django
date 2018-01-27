from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


# 功能测试
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        # Jason听说有一个很酷的在线待办事项应用
        # 他去看了这个应用的首页
        self.browser.get('http://localhost:8000/')

    def tearDown(self):
        self.browser.quit()

    def testWhenOpenDjangoThenDisplayTODOListAPP(self):
        # 他注意到网页的标题和头部都包含"To-Do"这个词
        self.assertIn('To-Do', self.browser.title)  # 判断前者是否后者的子字符串
        html_head = self.browser.find_element_by_tag_name("h1")
        self.assertIn('To-Do', html_head.text)
        # self.fail('Finish the test!')  # 无论如何,使测试失败并返回其中的字符串

    def testWhenOpenAppThenCanInputText(self):
        # 应用邀请他输入一个待办事项
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(input_box.get_attribute('placeholder'), 'Please enter your to-do item.')

    def testWhenInputAndEnterThenSaveItem(self):
        # 他在一个文本框中输入"learn django in a month"
        input_text = "learn django in a month"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys(input_text)
        # 他按回车键后,页面更新了
        input_box.send_keys(Keys.ENTER)
        # 待办事项表格中显示了"1.learn django in a month"
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        #self.assertTrue(any(row.text == input_text for row in rows),
        #                "New item did not appear in the table")
        self.assertIn("1. " + input_text, [row.text for row in rows])

    def testWhenInputAgainThenSaveSecondItem(self):
        # 页面中又显示了一个文本框,可以输入其他的待办事项
        # 他输入了"write a new virtual currency base on open source coin"
        input_text1 = "learn django in a month"
        input_text2 = "write a new virtual currency base on open source coin"
        count = 1
        # 页面再次更新,他的清单中显示了这两个待办事项
        self.check_for_row_in_list_table(input_text1, count)
        count = count + 1
        self.check_for_row_in_list_table(input_text2, count)

    def check_for_row_in_list_table(self, row_text, count):
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys(row_text)
        input_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(str(count) + ". " + row_text, [row.text for row in rows])

# Jason想知道这个网站是否会记住他的清单

# 他看到网站为他生成了一个惟一的url
# 而且页面中有些文字解说这个功能

# 他访问那个url,发现他的待办事项列表还在

if __name__ == '__main__':
    unittest.main()

    """django启动命令
    docker run --rm -v "$PWD":/usr/src/app -w /usr/src/app -p 8000:8000 -d django:1.7 bash -c "cd superlists && python3 manage.py runserver 0.0.0.0:8000"

    """
