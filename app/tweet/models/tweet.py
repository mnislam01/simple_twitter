from django.conf import settings
from django.db import models

from app.core.models.base import BaseModel

User = settings.AUTH_USER_MODEL


class Tweet(BaseModel):
    parent = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tweets"
    )
    likes = models.ManyToManyField(
        "tweet.TweetLikes",
        related_name="tweet_likes",
    )
    image = models.FileField(
        upload_to='images/',
        blank=True,
        null=True
    )
    post = models.CharField(
        max_length=300,
        default="",
    )

    def __str__(self):
        return self.post[:60]


class TweetLikes(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name="tweet_likes",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="liked_tweets"
    )

    def __str__(self):
        return f"{self.user.username} liked: {self.tweet.post[:60]}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tweet', 'user'], name='unique-like-per-tweet-and-user')
        ]
