from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SiteTest(TestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        options.add_argument('--verbose')
        self.browser = webdriver.Remote("http://selenium:4444", options=options)

    def tearDown(self):
        self.browser.quit()

    def test_visit_site(self):
        self.browser.get('http://django:8000')
        self.assertIn(self.browser.title, 'To-do lists')
        self.assertTemplateUsed(self.browser.page_source, "home.html")
