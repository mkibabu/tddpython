from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import unittest
import sys

class NewVisitorTest(StaticLiveServerTestCase):
    """
    Tests are organized into classes, which inherit from unittest.TestCase or its
    Django derivatives
    """
    def createBrowser(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path="/Users/mmuraya/.local/bin/Firefox.app/Contents/MacOS/firefox"))

    @classmethod
    def setUpClass(self):
        """Dirty hack to adapt tests to run on staging. LiveServerTestCase assumes we
        want to always use its test server. This hack makes it so that we can sometimes
        change that to use a different urls
        """
        for arg in sys.argv:
            if 'liveserver' in arg:
                self.server_url = 'http://{}'.format(arg.split('=')[1])
                return
        # we inherit from LiveServerTestCase; here's where it sets up the tet server
        super().setUpClass()
        self.server_url = self.live_server_url

    @classmethod
    def tearDownClass(self):
        if self.server_url == self.live_server_url:
            super().tearDownClass()

    """
    setUp and tearDown are restricted methods, used to initialize and clean up
    after each test.
    """
    def setUp(self):
        self.createBrowser()
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
        self.browser.get(self.server_url)

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
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')
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

        # New user comes along. Use a new browser session to ensure no session
        # info leaks through
        self.browser.quit()
        self.createBrowser()
        # New user visits home page. Ensure the first user's list isn't visible
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Eat more kale', page_text)
        self.assertNotIn('Play with the cat', page_text)

        # new user starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # new user gets a new list url
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(first_user_list_url, second_user_list_url)

        # confirm again that the first user's list is not visible
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Eat more kale', page_text)
        self.assertNotIn('Play with the cat', page_text)


    def test_layout_and_styling(self):
        """Tests that the static files (here, CSS) are loading, by checking one
        aspect of the layout. Testing design and layout should be avoided, since
        those change, but one can (and should) have a small 'smoke test' such as
        this one to make sure that static files are loaded.
        """
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                              512,
                              delta=5)

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
                               512,
                               delta = 5)
