from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def testWhenOpenRootUrlThenShowHomePage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
