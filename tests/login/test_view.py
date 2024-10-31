from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ...forms import LoginForm  # Assuming `LoginForm` is in `clients.forms`
from ...userauth import UserMiddleware01 
from ...accounts import AccountService01 # Importing custom middleware directly

User = get_user_model()

class LoginViewTest(TestCase):
    def setUp(self):
        # Set up a user for testing
        AccountService01.save_user_with_hashed_password(username='testuser', email='test@example.com', password='testpassword123')
        self.client = Client()
        self.login_url = reverse('login')

    def test_get_request_renders_login_form(self):
        """Test GET request renders login form template with a form context."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/login.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_post_ajax_valid_credentials(self):
        """Test that a valid AJAX POST request returns a success JSON response."""
        response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'testpassword123'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'success': True, 'redirect_url': reverse('dashboard')}
        )

    def test_post_ajax_invalid_credentials(self):
        """Test that an AJAX POST request with invalid credentials returns an error JSON response."""
        response = self.client.post(
            self.login_url,
            {'username': 'wronguser', 'password': 'wrongpassword'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {'success': False, 'message': 'Invalid username or password.'}
        )

    def test_post_non_ajax_valid_credentials(self):
        """Test that a valid non-AJAX POST request redirects to the register page."""
        response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'testpassword123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('register'))

    def test_post_non_ajax_invalid_credentials(self):
        """Test that an invalid non-AJAX POST request returns the login form with an error."""
        response = self.client.post(
            self.login_url,
            {'username': 'wronguser', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
