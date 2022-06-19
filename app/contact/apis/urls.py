
from django.urls import path

from app.contact.apis.views import (
    LoginAPIView,
    RegisterAPIView,
    LogoutAPIView,
    FollowUserAPIView,
    UnfollowUserAPIView,
    ProfileAPIView
)

app_name = "contact"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login-api-view"),
    path("register/", RegisterAPIView.as_view(), name="register-api-view"),
    path("logout/", LogoutAPIView.as_view(), name="logout-api-view"),
    path("follow/", FollowUserAPIView.as_view(), name="follow-api-view"),
    path("unfollow/", UnfollowUserAPIView.as_view(), name="unfollow-api-view"),
    path("profile/", ProfileAPIView.as_view(), name="profile-api-view")
]
