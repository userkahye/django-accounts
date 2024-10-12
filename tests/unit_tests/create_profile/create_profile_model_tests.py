from django.test import TestCase
from ....models import Client
from django.db import IntegrityError

class ClientModelTests(TestCase):

    def setUp(self):
        """Initialize common data for tests."""
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'validpassword123'
        self.create_client(self.username, self.email, self.password)

    def create_client(self, username, email, password):
        """Helper method to create and return a client instance."""
        return Client.objects.create(username=username, email=email, password=password)

    def test_create_client(self):
        """Test that a client can be created successfully."""
        client = Client.objects.get(username=self.username)
        self.assertIsInstance(client, Client)
        self.assertEqual(client.username, self.username)

    def test_duplicate_username(self):
        """Test that an IntegrityError is raised for duplicate usernames."""
        with self.assertRaises(IntegrityError):
            self.create_client(self.username, 'new@example.com', self.password)

    def test_duplicate_email(self):
        """Test that an IntegrityError is raised for duplicate emails."""
        with self.assertRaises(IntegrityError):
            self.create_client('newuser', self.email, self.password)
