from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass321'
        username = 'test1'
        first_name = 'Kerei'
        last_name = 'Musungu'
        user = get_user_model().objects.create_user(
            email=email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raise_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('John','Doe','john_doe', '','test123')
