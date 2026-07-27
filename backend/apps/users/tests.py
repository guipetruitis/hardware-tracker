from django.test import TestCase
from .models import User

# Create your tests here.
class UserModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        user = User.objects.create_user(
            email = "test@example.com",
            password = "testpass123")

        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError): 
            User.objects.create_user(
                email = "",
                password = "testpass123"
            )

    def test_create_superuser_successful(self):
        superuser = User.objects.create_superuser(
            email = "test1@example.com",
            password = "testpass1234")

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

