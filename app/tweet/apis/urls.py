
from django.urls import path

from app.tweet.apis.views import TweetListAPIView, NewsFeedAPIView, TweetCreateAPIView, TweetReactionAPIView

app_name = "tweet"

urlpatterns = [
    path("", TweetListAPIView.as_view(), name="tweet-list-api-view"),
    path("new/", TweetCreateAPIView.as_view(), name="tweet-create-api-view"),
    path("newsfeed/", NewsFeedAPIView.as_view(), name="newsfeed-api-view"),
    path("<uuid:uuid>/reaction/", TweetReactionAPIView.as_view(), name="reaction-api-view"),
]
