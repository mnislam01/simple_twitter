from rest_framework.exceptions import ValidationError

from app.contact.models import Profile
from django.contrib.auth import get_user_model, authenticate, logout

from app.core.service import BaseService


class ContactService(BaseService):
    model = Profile

    def create_profile(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def get_profile_by_user(self, user):
        return user.profile

    def authorize_user(self, **kwargs):
        user = authenticate(**kwargs)
        if user is None:
            raise ValidationError(
                'A user with this username and password is not found.'
            )
        return user

    def logout_user(self, request):
        logout(request)

    def user_post_save(self, user_instance):
        profile_data = {
            "user_id": user_instance.id,
        }
        self.create_profile(**profile_data)

    def user_follow(self, user_profile, **kwargs):
        user = get_user_model().objects.get(username=kwargs.get("username"))
        user_profile.following.add(user)
        user.profile.followers.add(user_profile.user)

    def user_unfollow(self, user_profile, **kwargs):
        user = get_user_model().objects.get(username=kwargs.get("username"))
        user_profile.following.remove(user)
        user.profile.followers.remove(user_profile.user)
