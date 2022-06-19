import pytest
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from app.tweet.models import Tweet
from app.utils import get_user_object

User = get_user_model()


@pytest.mark.django_db
class TestTweetCreateAPI:
    url = reverse("api:tweet_apis:tweet-create-api-view")

    def test_tweet_create_api_view(self):
        client = APIClient()
        user = get_user_object(username="test.user", password="!@#$%QWERT")
        client.login(username="test.user", password="!@#$%QWERT")
        payload = {
            "post": "Satoshi Nakamoto is an alien"
        }
        response = client.post(self.url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["post"] == payload["post"]


@pytest.mark.django_db
class TestTweetListAPI:
    url = reverse("api:tweet_apis:tweet-list-api-view")

    def test_tweet_list_api_view(self):
        client = APIClient()
        user = get_user_object(username="test.user", password="!@#$%QWERT")
        client.login(username="test.user", password="!@#$%QWERT")
        payload = {
            "post": "Satoshi Nakamoto is an alien"
        }
        tweet_create = client.post(reverse("api:tweet_apis:tweet-create-api-view"), payload)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) > 0


@pytest.mark.django_db
class TestTweetListAPI:
    url = reverse("api:tweet_apis:newsfeed-api-view")

    def test_tweet_list_api_view(self):
        client = APIClient()
        user1 = get_user_object(username="test.user1", password="!@#$%QWERT")
        user2 = get_user_object(username="test.user2", password="!@#$%QWERT")
        client.login(username="test.user1", password="!@#$%QWERT")
        payload = {
            "post": "Satoshi Nakamoto is an alien"
        }
        tweet_create = client.post(reverse("api:tweet_apis:tweet-create-api-view"), payload)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTweetNewsFeedAPI:
    url = reverse("api:tweet_apis:newsfeed-api-view")

    def test_tweet_newsfeed_api_view(self):
        client = APIClient()
        user1 = get_user_object(username="test.user1", password="!@#$%QWERT")
        user2 = get_user_object(username="test.user2", password="!@#$%QWERT")
        t = Tweet.objects.create(user=user2, post="Satoshi Nakamoto is an alien")
        user1.profile.following.add(user2)
        user2.profile.followers.add(user1)

        client.login(username="test.user1", password="!@#$%QWERT")

        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTweetLikeAPI:

    def test_tweet_like_api_view(self):
        user1 = get_user_object(username="test.user1", password="!@#$%QWERT")
        client = APIClient()
        client.login(username="test.user1", password="!@#$%QWERT")
        t = Tweet.objects.create(user=user1, post="Satoshi Nakamoto is an alien")
        url = reverse("api:tweet_apis:reaction-api-view", kwargs={"uuid": t.uuid})
        payload = {
            "user_id": user1.id,
            "new_like": True,
        }
        response = client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
