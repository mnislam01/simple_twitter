from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.contact.apis.serializers import (
    RegisterSerializer,
    LoginSerializer,
    FollowSerializer,
    UnFollowSerializer,
    ProfileSerializer,
    LogoutSerializer
)
from app.contact.services.contact_service import ContactService


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    service_class = ContactService

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        service = self.service_class()
        service.authorize_user(**serializer.validated_data)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    service_class = ContactService

    def create(self, request, *args, **kwargs):
        service = self.service_class()
        service.logout_user(request=request)
        return Response(data={"Logged out."}, status=status.HTTP_200_OK)


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    service_class = ContactService

    def perform_create(self, serializer):
        service = self.service_class()
        user = serializer.save()
        service.user_post_save(user_instance=user)


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    service_class = ContactService

    def get_object(self):
        service = self.service_class()
        return service.get_profile_by_user(user=self.request.user)


class FollowUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FollowSerializer
    service_class = ContactService

    def perform_create(self, serializer):
        service = self.service_class()
        user_profile = self.request.user.profile
        service.user_follow(user_profile=user_profile, **serializer.validated_data)


class UnfollowUserAPIView(generics.CreateAPIView):
    serializer_class = UnFollowSerializer
    service_class = ContactService

    def perform_create(self, serializer):
        service = self.service_class()
        user_profile = self.request.user.profile
        service.user_unfollow(user_profile=user_profile, **serializer.validated_data)

