from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsProfileUser
from users.serializers import UserSerializer, UserRegisterSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]
