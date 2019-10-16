from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer
import pytest

TAGS_URL = reverse('recipe:tag-list')


@pytest.fixture
def setup_client():
    return APIClient()


@pytest.fixture
def setup_user(setup_client):
    client = setup_client
    user = get_user_model().objects.create_user(
        'test@gmail.com',
        'testpass'
    )
    client.force_authenticate(user)
    return user


@pytest.mark.django_db
class TestPublicTagApi():
    """Test the publicly available tags API"""

    def test_login_required(self, setup_client):
        """Test that login is required for retrieving tags"""
        client = setup_client
        res = client.get(TAGS_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateTagsApi():
    """Test the authorized user tags api"""

    def test_retrieve_tags(self, setup_client, setup_user):
        """Test retrieving tags"""
        client = setup_client
        user = setup_user
        Tag.objects.create(user=user, name='Vegan')
        Tag.objects.create(user=user, name='Dessert')
        res = client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_tags_limited_to_user(self, setup_client, setup_user):
        """Test that tags returned are for the authenticated user"""
        client = setup_client
        user = setup_user
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=user, name='Comfort food')
        res = client.get(TAGS_URL)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert (res.data[0]['name'] == tag.name)

    def test_create_tags_successfull(self, setup_client, setup_user):
        """Test creating new tag"""
        client = setup_client
        user = setup_user
        payload = {
            'name': 'Test tag'
        }
        client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=user,
            name=payload['name']
        ).exists()
        assert exists

    def test_create_tag_invalid(self, setup_client, setup_user):
        """Test try to create an invalid tag"""
        client = setup_client
        payload = {
            'name': ''
        }
        res = client.post(TAGS_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
