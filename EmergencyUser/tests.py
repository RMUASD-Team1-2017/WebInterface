from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse

def test_retrieve(page_type, kwargs = {}):
        print("Testing retrievement of %s" % (page_type))
        c = Client()
        if len(kwargs):
            return c.get(reverse("EmergencyUser:{}".format(page_type), kwargs = kwargs) ).status_code
        return c.get(reverse("EmergencyUser:{}".format(page_type)) ).status_code

class PageRetrieveTests(TestCase):
#Simple test to see if we can retrieve the webpages

    def test_dispatch_page(self):
        self.assertEqual(test_retrieve("drone_dispatch"), 200)
