
from django.conf import settings
from django.db import models

from app.core.models.base import BaseModel

User = settings.AUTH_USER_MODEL


def save_db_to(instance, filename):
    return f"profile_{instance.user.id}/{filename}"


class Profile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    followers = models.ManyToManyField(
        User,
        related_name="followers",
        blank=True,
    )
    following = models.ManyToManyField(
        User,
        related_name="following",
        blank=True,
    )
    display_picture = models.ImageField(
        upload_to=save_db_to,
        null=True,
        blank=True,
    )
    about = models.TextField(
        default="",
        blank=True,
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
