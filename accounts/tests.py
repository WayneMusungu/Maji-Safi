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

    def test_new_user_without_username_raise_error(self):
        """Test that creating a user without a username raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('John','Doe','', 'john@gmail.com','test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test@example.com'
        password = 'testpass321'
        username = 'test1'
        first_name = 'Christabel'
        last_name = 'Phoebe'
        user = get_user_model().objects.create_superuser(
            email=email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password
        )

        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superadmin)



class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            password='password'
        )

    def test_create_user(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get(email='test@example.com').username, 'testuser')

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            first_name='Test',
            last_name='Superuser',
            username='testsuperuser',
            email='superuser@example.com',
            password='password'
        )

        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superadmin)

    def test_get_role(self):
        user = get_user_model().objects.get(email='test@example.com')
        user.role = 1
        self.assertEqual(user.get_role(), 'Supplier')
        user.role = 2
        self.assertEqual(user.get_role(), 'Customer')

