from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
class TestUserCreation:
    def test_create_user_with_email_successfull(self):
        """
        Test creating a new user with an email is successfull
        """
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        assert user.email == email
        assert user.check_password(password)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password="Testpass123"
        )
        assert user.email == email.lower()

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with pytest.raises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="testpass123"
            )

    def test_create_new_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            email='test@gmail.com',
            password='testpass123',
        )
        assert user.is_superuser
        assert user.is_staff
