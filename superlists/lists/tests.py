from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    def testWhenOpenRootUrlThenShowHomePage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def testWhenOpenHomepageThenShowRightHtml(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(render_to_string('home.html'), response.content.decode())


class LiveViewTest(TestCase):
    def testWhenRedirectNewUrlThenDisplayOnlyItemsForTheList(self):
        input_text1 = 'first item in new url'
        input_text2 = 'second item in new url'

        list_one = List.objects.create()
        Item.objects.create(text=input_text1, list=list_one)
        Item.objects.create(text=input_text2, list=list_one)

        list_two = List.objects.create()
        Item.objects.create(text="something else 1", list=list_two)
        Item.objects.create(text="something else 2", list=list_two)

        response = self.client.get('/lists/%d/' % (list_one.id,))

        self.assertContains(response, input_text1)
        self.assertContains(response, input_text2)
        self.assertNotContains(response, "something else 1")
        self.assertNotContains(response, "something else 2")

    def testUseDiffTemplate(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, template_name='list.html')

    def testPassCorrectListToTemplate(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def testWhenEnterThenSavePOSTRequest(self):
        input_text = 'a new item text'
        # 修改数据库的操作返回的新url不以斜杠结尾
        self.client.post('/lists/new', data={'item_text': input_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, input_text)

        # 怎么测试视图函数给new_item_text传入正确的值，又怎么把变量传入模板？
        # 使用render_to_string的第二个入参传递期望值给模板的变量来测试
        # 在视图函数中使用render的第三个入参传递请求的POST
        # expect_html = render_to_string('home.html',{'new_item_text': input_text})
        # self.assertEqual(expect_html, response.content.decode())

    def testWhenEnterThenRedirectToHome(self):
        input_text = 'a new item text'
        response = self.client.post('/lists/new', data={'item_text': input_text})
        # 发送请求后重定向
        self.assertEqual(response.status_code, 302)
        # 在回车后重定向页面到首页
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):
    # 把新的待办事项加入到现有的清单中,而不是一个url只保存一个待办事项
    def testWhenSavePOSTThenToExistingList(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        input_text = "first item for the list"
        self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text': input_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, input_text)
        self.assertEqual(new_item.list, correct_list)

    def testWhenEnterThenRedirectToListView(self):
        input_text = 'a new item text'
        new_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % (new_list.id,), data={'item_text': input_text})
        # 发送请求后重定向
        self.assertEqual(response.status_code, 302)
        # 在回车后重定向页面到清单列表页
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class ListAndItemModelTest(TestCase):
    def testSaveAndRetrievingItems(self):
        # 新建List对象，让待办事项和不同的清单关联起来
        list_ = List()  # 使用list_是为了区别于原生list函数
        list_.save()

        first_item = Item()
        first_item.text = 'the first list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_saved_item.list, list_)
