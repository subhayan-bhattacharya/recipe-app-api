from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(
        **params
    )


@pytest.fixture()
def setup_client():
    client = APIClient()
    return client


@pytest.mark.django_db
def test_create_valid_user_success(setup_client):
    """Test create user with valid user is successfull"""
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'testpass',
        'name': 'Test name'
    }
    res = client.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(**res.data)
    assert user.check_password(payload['password'])
    assert 'password' not in res.data


@pytest.mark.django_db
def test_user_exists(setup_client):
    """Test creating user that already exists fails"""
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'testpass',
        'name': 'Test name'
    }
    create_user(**payload)
    res = client.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_is_to_short(setup_client):
    """Test that password must be more than 5 characters"""
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'pw',
        'name': 'Test name'
    }
    res = client.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model().objects.filter(
        email=payload['email']).exists()
    assert not user_exists


@pytest.mark.django_db
def test_create_token_for_user(setup_client):
    """Test that a user token is successfully created"""
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'testpass',
    }
    create_user(**payload)
    res = client.post(TOKEN_URL, payload)
    assert "token" in res.data
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_token_invalid_credentials(setup_client):
    """
    Test that a user when supplies invalid credentials
    token is not created
    """
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'testpass',
    }
    create_user(**payload)
    payload["password"] = "Something else"
    res = client.post(TOKEN_URL, payload)
    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_token_no_user(setup_client):
    """Test that token is not created when there is no user"""
    client = setup_client
    payload = {
        'email': 'test@gmail.com',
        'password': 'testpass',
    }
    res = client.post(TOKEN_URL, payload)
    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_token_missing_field(setup_client):
    """Test token is not created when the password is missing"""
    client = setup_client
    res = client.post(TOKEN_URL, {"email": "test@gmail.com"})
    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST
