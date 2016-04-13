from selenium import webdriver
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
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        inputbox.send_keys('Keys.ENTER')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1. Eat more kale' for row in rows),
                "New to-do item did not appear in table"
        )
        # There is still a test box prompting to add another item. Add 'Play with the
        # cat'.
        self.fail('Finish the test!')

        # Page updates again, and now both items are on the list.
        
        # Site generates a unique url for the user's list.
        
        # User visits that url; list is still there.

"""
The 'if __name__ == '__main__' clause is used to determine whether the script has
been called from the command lne, rather than just imported by another script.
Here, we use it to suppress a potential superfluous ResourceWarning error message.
"""
if __name__ == '__main__':
    unittest.main(warnings='ignore')
