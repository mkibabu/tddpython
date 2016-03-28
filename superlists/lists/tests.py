from django.test import TestCase
# while functional_tests.py imported unittest and inherits from unittest.TestCase,
# Django helpfully suggests that we us a special version of TestCase, which it comes
# bundled with.

# Create your tests here.


# Deliberately silly etst, to test the automated test runner. The automated test
# runner is a manage.py command, 'test'.
class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
