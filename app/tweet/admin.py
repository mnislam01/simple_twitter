from django.contrib import admin

from app.tweet.models import Tweet
from app.tweet.models.tweet import TweetLikes

admin.site.register(Tweet)
admin.site.register(TweetLikes)
