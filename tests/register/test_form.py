from django.test import TestCase
from ...forms import RegistrationForm
from ...models import Client

class RegistrationFormTests(TestCase):

    def setUp(self):

        Client.objects.create(username='existinguser', email='user@example.com', password='Password123!')

    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_too_short(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'short'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'], ["Password must be at least 8 characters long."])

    def test_username_already_exists(self):
        form_data = {
            'username': 'existinguser',  # This username already exists
            'email': 'newuser@example.com',
            'password': 'Password123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["Username already exists."])

    def test_email_already_exists(self):
        form_data = {
            'username': 'newuser',
            'email': 'user@example.com',  # This email already exists
            'password': 'Password123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Email already exists."])

    def test_username_case_insensitive(self):
        form_data = {
            'username': 'EXISTINGUSER',  # This username should fail because of case insensitivity
            'email': 'newuser2@example.com',
            'password': 'Password123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["Username already exists."])

    def test_email_case_insensitive(self):
        form_data = {
            'username': 'newuser3',
            'email': 'USER@EXAMPLE.COM',  # This email should fail because of case insensitivity
            'password': 'Password123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["Email already exists."])
