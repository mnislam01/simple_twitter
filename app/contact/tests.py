import pytest
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from app.contact.models import Profile
from app.utils import get_user_object

User = get_user_model()


@pytest.fixture()
def registration_api_payload():
    return {
        "username": "test.user",
        "first_name": "John",
        "last_name": "Doe",
        "password": "!@#$%QWERT",
        "password2": "!@#$%QWERT"
    }


@pytest.fixture()
def login_api_payload_wrong():
    return {
        "username": "test.user1",
        "password": "12345qwert",
    }


@pytest.fixture()
def login_api_payload_right():
    return {
        "username": "test.user2",
        "password": "!@#$%QWERT",
    }



@pytest.mark.django_db
class TestRegistrationAPI:
    url = reverse("api:contact_apis:register-api-view")

    def test_user_registration_api_view_status(self, registration_api_payload):
        client = APIClient()
        response = client.post(self.url,  registration_api_payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_registration_new_user_check(self, registration_api_payload):
        client = APIClient()
        old_state = User.objects.count()
        client.post(self.url, registration_api_payload)
        new_state = User.objects.count()
        assert new_state > old_state

    def test_user_registration_check_profile(self, registration_api_payload):
        client = APIClient()
        client.post(self.url, registration_api_payload)
        user = User.objects.get(username="test.user")
        assert user.profile


@pytest.mark.django_db
class TestLoginAPI:
    url = reverse("api:contact_apis:login-api-view")

    def test_login_api_view_with_wrong_credentials(self, login_api_payload_wrong):
        user = User.objects.create(username="test.user1")
        user.set_password("!@#$%QWERT")
        user.save()
        client = APIClient()
        response = client.post(self.url,  login_api_payload_wrong)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_api_view_with_right_credentials(self, login_api_payload_right):
        user = User.objects.create(username="test.user2")
        user.set_password("!@#$%QWERT")
        user.save()
        client = APIClient()
        response = client.post(self.url, login_api_payload_right)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestProfileAPI:
    url = reverse("api:contact_apis:profile-api-view")

    def test_profile_api_view(self):
        user = User.objects.create(username="test.user2")
        user.set_password("!@#$%QWERT")
        user.save()
        Profile.objects.create(user=user)
        client = APIClient()
        client.login(username='test.user2', password='!@#$%QWERT')
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestFollowAPI:
    url = reverse("api:contact_apis:follow-api-view")

    def test_follow_api_view(self):
        user1 = get_user_object(username="user.text1", password="!@#$%QWERT")
        user2 = get_user_object(username="user.text2", password="!@#$%QWERT")
        client = APIClient()
        client.login(username='user.text1', password='!@#$%QWERT')
        payload = {
            "username": "user.text2",

        }
        response = client.post(self.url, payload)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUnFollowAPI:
    url = reverse("api:contact_apis:unfollow-api-view")

    def test_unfollow_api_view(self):
        user1 = get_user_object(username="user.text1", password="!@#$%QWERT")
        user2 = get_user_object(username="user.text2", password="!@#$%QWERT")
        client = APIClient()
        client.login(username='user.text1', password='!@#$%QWERT')
        payload = {
            "username": "user.text2",
        }
        response = client.post(self.url, payload)
        assert response.status_code == status.HTTP_201_CREATED
