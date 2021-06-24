from time import sleep, time
from selenium import webdriver
import unittest

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase

MAX_WAIT = 3


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.chrome_config = Options()
        self.chrome_config.headless = True
        self.chrome_config.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        self.browser = webdriver.Chrome(options=self.chrome_config)

    def tearDown(self) -> None:
        self.browser.close()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(
                    row_text,
                    [row.text for row in rows],
                    f"New to-do item did not appear in table. Contents were:\n{table.text}",
                )
                return
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT:
                    raise e
                sleep(0.25)

    def test_can_start_a_list_for_one_user(self):
        # Go to a web address for the project page
        self.browser.get(self.live_server_url)

        # Verify that we are on the right page
        # assert 'To-do' in self.browser.title
        self.assertIn("To-do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-do", header_text)

        # Isaac sees there is a way to enter a new to do item
        input_box = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # Isaac types 'Sell the gold nuggets' into a line field
        input_box.send_keys("Sell the gold nuggets")

        # When she hits enter, the page updates, and now the page lists
        # "1: Sell the gold nuggets" as an item in a to-do list table
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Sell the gold nuggets")

        # Isaac enters "Wash the golden goose"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Wash the golden goose")
        input_box.send_keys(Keys.ENTER)

        # Isaac sees two entered items
        self.wait_for_row_in_list_table("1: Sell the gold nuggets")
        self.wait_for_row_in_list_table("2: Wash the golden goose")

        # Isaac wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # Isaac visits that URL - her to-do list is still there.

        # Satisfied, Isaac goes back to sleep
        # self.fail("Finish the test!")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Go to a web address for the project page
        self.browser.get(self.live_server_url)

        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Sell the gold nuggets")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Sell the gold nuggets")

        # She enters "Wash the golden goose"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Wash the golden goose")
        input_box.send_keys(Keys.ENTER)

        # She notices that her list has a unique URL
        jane_list_url = self.browser.current_url
        self.assertRegex(jane_list_url, "/lists/.+")

        # # We use a new browser session to make sure that no information
        # # of Jane's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Chrome(options=self.chrome_config)

        # Francis visits the home page. There is no sign of Jane's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Sell the gold nuggets", page_text)
        self.assertNotIn("golden goose", page_text)

        # Francis starts a new list by entering a new item. He is less interesting than Jane...
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, jane_list_url)

        # Again, there is no trace of Jane's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
        # Satisfied, they both go back to sleep
