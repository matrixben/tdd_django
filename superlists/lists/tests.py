from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def testWhenOpenRootUrlThenShowHomePage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def testWhenOpenHomepageThenShowRightHtml(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(render_to_string('home.html'), response.content.decode())

    def testWhenEnterThenSavePOSTRequest(self):
        input_text = 'a new item text'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = input_text
        # 怎么测试视图函数给new_item_text传入正确的值，又怎么把变量传入模板？
        response = home_page(request)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, input_text)

        # 使用render_to_string的第二个入参传递期望值给模板的变量来测试
        # 在视图函数中使用render的第三个入参传递请求的POST
        #expect_html = render_to_string('home.html',{'new_item_text': input_text})
        #self.assertEqual(expect_html, response.content.decode())

    def testWhenEnterThenRedirectToHome(self):
        input_text = 'a new item text'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = input_text
        response = home_page(request)
        # 在回车后重定向页面到首页
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def testOnlyInputSomethingThenSaveIntoDB(self):
        request = HttpRequest()
        home_page(request)
        # 没有输入待办事项时不保存数据库
        self.assertEqual(Item.objects.count(), 0)

    def testWhenEnterSecondItemThenShowAllLItems(self):
        # 输入第二个待办事项后显示全部两个事项,测试将数据库的值传给模板变量
        input_text1 = 'first item'
        input_text2 = 'second item'

        Item.objects.create(text=input_text1)
        Item.objects.create(text=input_text2)

        request = HttpRequest()
        response = home_page(request)

        self.assertIn(input_text1, response.content.decode())
        self.assertIn(input_text2, response.content.decode())


class ItemModelTest(TestCase):
    def testSaveAndRetrievingItems(self):
        first_item = Item()
        first_item.text = 'the first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)
