from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from app.contact.models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):          # noqa
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)


class LogoutSerializer(serializers.Serializer):      # noqa
    ...


class FollowSerializer(serializers.Serializer):        # noqa
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class UnFollowSerializer(serializers.Serializer):       # noqa
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name"
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user_data")
    followers = serializers.SerializerMethodField(method_name="get_follower_numbers")
    following = serializers.SerializerMethodField(method_name="get_following_numbers")

    class Meta:
        model = Profile
        fields = [
            "user",
            "followers",
            "following",
            "display_picture",
            "about"
        ]

    def get_user_data(self, obj):
        return UserSerializer(obj.user).data

    def get_follower_numbers(self, obj):
        return obj.followers.count()

    def get_following_numbers(self, obj):
        return obj.following.count()
