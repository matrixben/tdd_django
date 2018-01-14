from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from todolists.views import home_page


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
