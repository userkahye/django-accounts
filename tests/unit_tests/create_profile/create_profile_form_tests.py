from django.test import TestCase
from ....models import Client
from ....forms import RegistrationForm

class RegistrationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_username(self):
        Client.objects.create(username='testuser', email='test@example.com', password='securepassword123')
        form_data = {
            'username': 'testuser',
            'email': 'unique@example.com',
            'password': 'anotherpassword'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_duplicate_email(self):
        Client.objects.create(username='uniqueuser', email='test@example.com', password='securepassword123')
        form_data = {
            'username': 'anotheruser',
            'email': 'test@example.com',
            'password': 'securepassword'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_length(self):
        form_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'a' * 129  # 129 characters long
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
