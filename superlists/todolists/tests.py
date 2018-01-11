from django.test import TestCase
from django.urls.resolvers import get_resolver
from todolists.views import home_page


# 单元测试
class HomePageTest(TestCase):

    def testWhenOpenRootUrlThenResolveToHomePage(self):
        found = get_resolver('/')
        self.assertEqual(found.func, home_page)
