
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ....views import RegistrationView 

class URLTests(SimpleTestCase):

    def test_registration_url_resolves(self):
        """ Test if the registration URL resolves to the correct view """
        url = reverse('register')  # Use the name you assigned in urls.py
        self.assertEqual(resolve(url).func.view_class, RegistrationView)

    def test_registration_url_accessible(self):
        """ Test if the registration URL is accessible and returns a 200 status code """
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

