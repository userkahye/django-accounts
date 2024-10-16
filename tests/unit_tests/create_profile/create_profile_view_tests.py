# clients/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from ....forms import RegistrationForm
from ....models import Client

class RegistrationViewTests(TestCase):

    def setUp(self):
        self.url = reverse('register')

    def test_get_registration_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_post_valid_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword',
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'message': 'Registration successful!',
            'redirect_url': reverse('register')
        })
        self.assertTrue(Client.objects.filter(username='testuser').exists())

    def test_post_invalid_username(self):
        Client.objects.create(username='existinguser', email='existinguser@example.com', password='securepassword')
        data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'securepassword',
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            'success': False,
            'errors': {
                'username': ['Username already exists.']
            }
        })

    def test_post_invalid_email(self):
        Client.objects.create(username='user1', email='existingemail@example.com', password='securepassword')
        data = {
            'username': 'newuser',
            'email': 'existingemail@example.com',
            'password': 'securepassword',
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            'success': False,
            'errors': {
                'email': ['Email already exists.']
            }
        })

    def test_post_invalid_password(self):
        data = {
            'username': 'shortpassuser',
            'email': 'shortpassuser@example.com',
            'password': 'short',
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            'success': False,
            'errors': {
                'password': ['Password must be at least 8 characters long.']
            }
        })
