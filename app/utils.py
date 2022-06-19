from django.contrib.auth import get_user_model

from app.contact.models import Profile

User = get_user_model()


def get_user_object(username="", password=""):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    Profile.objects.create(user=user)
    return user
