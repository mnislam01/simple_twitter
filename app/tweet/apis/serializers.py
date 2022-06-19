from rest_framework import serializers

from app.tweet.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    likes = serializers.IntegerField(source="likes.count")

    class Meta:
        model = Tweet
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "username",
            "likes",
            "post",
            "image"
        ]


class TweetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = [
            "image",
            "post"
        ]


class TweetLikeSerializer(serializers.Serializer):  # noqa
    user_id = serializers.IntegerField(required=True, allow_null=False)
    new_like = serializers.BooleanField(required=True, allow_null=False)
