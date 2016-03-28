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
        self.fail('Finish the test!')
        
        # See prompt to enter a to-do item
        
        # Enter a to-do item: 'Eat more kale'
        
        # Hit enter, and page updates, and lists
        # '1. Eat more kale' as an item on the to-do list
        
        # There is still a test box prompting to add another item. Add 'Play with the
        # cat'.
        
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
