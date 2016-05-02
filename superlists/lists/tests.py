from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page

# Django's workflow: MVC, where views are more like controllers, and templates are
# actually the views. When a HTTP request comes in, Django uses rules to figure out
# which view function to call (this is called "resolving the url". The view function
# then processes the url and returns a http response.

# Here, we create a test to resolve the root of the site ("/") and return a HTTP 
# response.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        # Django's resolve('path') function is used to resolve urls. We'll use it
        # to check that '/' resolves to a function called home_page
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Test list entry'

        response = home_page(request)

        self.assertIn('Test list entry', response.content.decode())
        expected_html = render_to_string ('home.html',
                { 'new_item_text': 'Test list entry' }
        )
        self.assertEqual(response.content.decode(), expected_html)
