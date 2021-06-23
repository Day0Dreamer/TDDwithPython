from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.close()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to a web address for the project page
        self.browser.get('http://localhost:8000')

        # Verify that we are on the right page
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test!')

        # Isaac sees there is a way to enter a new to do item

        # Isaac types 'Sell the gold nuggets' into a line field

        # Isaac sees another line to enter another to do item

        # Isaac enters "Wash the golden goose"

        # Isaac sees two entered items

        # Isaac wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # Isaac visits that URL - her to-do list is still there.

        # Satisfied, Isaac goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
