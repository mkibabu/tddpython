from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest

class NewVisitorTest(unittest.TestCase):
    """
    Tests are organized into classes, which inherit from unittest.TestCase
    """

    """
    setUp and tearDown are restricted methods, used to initialize and clean up
    after each test.
    """
    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path="/Users/mmuraya/.local/bin/Firefox.app/Contents/MacOS/firefox"))
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    """
    Little helper method that checks for text in the table
    """
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    """
    Test methods must start with the word "test", and should have a descriptive name.
    """
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to the To-Do app's home page
        self.browser.get('http://localhost:8000')
        
        # Verify the page title mentions 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Find prompt to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # Enter a to-do item: 'Eat more kale'
        inputbox.send_keys('Eat more kale')
        # Hit enter, and page updates, and lists
        # '1. Eat more kale' as an item on the to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1. Eat more kale')
        # There is still a test box prompting to add another item. Add 'Play with the
        # cat'.
        # since page refreshed, Selenium has lost reference to elements
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play with the cat')
        inputbox.send_keys(Keys.ENTER)

        # Page updates again, and now both items are on the list.
        self.check_for_row_in_list_table('1. Eat more kale')
        self.check_for_row_in_list_table('2. Play with the cat')
        # Site generates a unique url for the user's list.
        
        # User visits that url; list is still there.

        self.fail('Finish the test!')
"""
The 'if __name__ == '__main__' clause is used to determine whether the script has
been called from the command line, rather than just imported by another script.
"""
if __name__ == '__main__':
    unittest.main(warnings='ignore')
