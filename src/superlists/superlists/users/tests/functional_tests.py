from time import sleep
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        chrome_config = Options()
        chrome_config.headless = True
        self.browser = webdriver.Chrome(options=chrome_config)

    def tearDown(self) -> None:
        self.browser.close()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to a web address for the project page
        self.browser.get("http://localhost:8000")

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
        sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(
            "1: Sell the gold nuggets",
            [row.text for row in rows],
            f"New to-do item did not appear in table. Contents were:\n{table.text}",
        )

        # Isaac enters "Wash the golden goose"
        input_box = self.browser.find_element_by_id("id_new_item")
        input_box.send_keys("Wash the golden goose")
        input_box.send_keys(Keys.ENTER)
        sleep(1)

        # Isaac sees two entered items
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(
            "1: Sell the gold nuggets",
            [row.text for row in rows],
            f"New to-do item did not appear in table. Contents were:\n{table.text}",
        )
        self.assertIn(
            "2: Wash the golden goose",
            [row.text for row in rows],
            f"New to-do item did not appear in table. Contents were:\n{table.text}",
        )

        # Isaac wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # Isaac visits that URL - her to-do list is still there.

        # Satisfied, Isaac goes back to sleep
        self.fail("Finish the test!")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
