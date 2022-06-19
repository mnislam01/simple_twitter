from app.core.service import BaseService
from app.tweet.models import Tweet
from app.tweet.models.tweet import TweetLikes


class TweetService(BaseService):
    model = Tweet

    def user_tweets(self, user):
        return self.model.objects.filter(user_id=user.id)

    def create_tweet(self, user, **kwargs):
        data = {
            "user_id": user.id,
        }
        data.update(kwargs)
        return self.model.objects.create(**data)

    def get_news_feed_tweets(self, user):
        news_feed_qs = self.model.objects.none()
        profile = user.profile
        for user in profile.following.all():
            news_feed_qs = news_feed_qs | user.tweets.all()
        return news_feed_qs.order_by("-created_at")

    def toggle_like(self, tweet_uuid, **kwargs):
        tweet = self.model.objects.get(uuid=tweet_uuid)
        if kwargs.get("new_like", False):
            tl = TweetLikes.objects.create(tweet_id=tweet.id, user_id=kwargs.get("user_id"))
            tweet.likes.add(tl)
        else:
            tl = TweetLikes.objects.filter(tweet_id=tweet.id, user_id=kwargs.get("user_id")).first()
            # guaranteed to be one
            if tl:
                tweet.likes.remove(tl)
                tl.delete()
