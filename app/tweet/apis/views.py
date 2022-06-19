from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from app.tweet.apis.serializers import TweetSerializer, TweetCreateSerializer, TweetLikeSerializer
from app.tweet.services.tweet_service import TweetService


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetSerializer
    service_class = TweetService

    def get_queryset(self):
        service = self.service_class()
        return service.user_tweets(user=self.request.user)


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetCreateSerializer
    service_class = TweetService

    def perform_create(self, serializer):
        service = self.service_class()
        service.create_tweet(user=self.request.user, **serializer.validated_data)


class NewsFeedAPIView(generics.ListAPIView):
    serializer_class = TweetSerializer
    service_class = TweetService

    def get_queryset(self):
        service = self.service_class()
        return service.get_news_feed_tweets(user=self.request.user)


class TweetReactionAPIView(generics.CreateAPIView):
    serializer_class = TweetLikeSerializer
    service_class = TweetService

    def perform_create(self, serializer):
        service = self.service_class()
        service.toggle_like(tweet_uuid=self.kwargs.get("uuid"), **serializer.validated_data)
