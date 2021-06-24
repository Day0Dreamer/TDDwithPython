from lists.models import Item, List
from django.urls import resolve
from django.db import models
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ItemAndListModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()  # type: models.Model
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()  # type: models.Model
        second_item.text = "The second list item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "The second list item")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_used_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="primary list itemey 1", list=correct_list)
        Item.objects.create(text="primary list itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list itemey 1", list=other_list)
        Item.objects.create(text="other list itemey 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "primary list itemey 1")
        self.assertContains(response, "primary list itemey 2")
        self.assertNotContains(response, "other list itemey 1")
        self.assertNotContains(response, "other list itemey 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        list_ = List.objects.create()
        self.client.post(
            "/lists/new/", data={"item_text": "A test list item"}, list=list_
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A test list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            "/lists/new/", data={"item_text": "A test list item"}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_.id}/")


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f"/lists/{correct_list.id}/add_item/",
            data={"item_text": "A new item for an existing list"},
        )
        self.client.post(
            f"/lists/{correct_list.id}/add_item/",
            data={"item_text": "A second item for an existing list"},
        )
        self.assertEqual(Item.objects.count(), 2)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f"/lists/{correct_list.id}/add_item/",
            data={"item_text": "A new item for an existing list"},
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
