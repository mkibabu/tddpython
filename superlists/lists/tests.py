from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
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

        # check that the list entry has been saved to the db.
        # objects.count() is shorthand for objects.all().count()
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Test list entry')

    def test_home_page_redirects_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Test list entry'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request =  HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_items_in_list(self):
        Item.objects.create(text='First item in list')
        Item.objects.create(text='Second item in list')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('First item in list', response.content.decode())
        self.assertIn('Second item in list', response.content.decode())

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)

