from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A test list item"})
        self.assertIn("A test list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
