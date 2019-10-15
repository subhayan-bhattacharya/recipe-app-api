from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest

CREATE_USER_URL = reverse('user:create')


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
    payload = {
        'email': 'test@gmail.com',
        'password': 'pw',
        'name': 'Test name'
    }
    res = client.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model.objects.get(email=payload['email']).exists()
    assert not user_exists
