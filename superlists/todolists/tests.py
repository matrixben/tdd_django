from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from todolists.views import home_page
from todolists.models import Item


# 单元测试
class HomePageTest(TestCase):

    def testWhenOpenRootUrlThenResolveToHomePage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def testWhenOpenHomePageThenReturnCorrectHtml(self):
        # 不要测试常量，应该测试实现的方式
        request = HttpRequest()
        response = home_page(request)
        expect_html = render_to_string('home.html')
        self.assertEqual(expect_html, response.content.decode()) #把字节转为字符串

    def testWhenSendEnterThenSavePostRequest(self):
        item_str = "a new item"
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = item_str

        response = home_page(request)
        self.assertIn(item_str, response.content.decode())
        # 将模板页面转为字符串，并将其中的变量用常量替换
        expect_html = render_to_string('home.html',{'new_item_text': item_str})
        self.assertEqual(expect_html, response.content.decode())
        # 将输入的待办事项保存到数据库
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, item_str)

    def testSavingAndRetievingItems(self):
        first_item = Item()
        first_item.text = "The first list item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[1].text, second_item.text)

    def testOnlySaveItemWhenNecessary(self):
        request = HttpRequest()
        home_page(request)
        # 没有输入待办事项时数据库没有记录
        self.assertEqual(Item.objects.count(), 0)
