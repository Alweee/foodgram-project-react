from djoser.serializers import (UserCreateSerializer, TokenCreateSerializer,
                                UserSerializer)

from rest_framework import serializers

from users.models import User, Subscription


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomTokenCreateSerializer(TokenCreateSerializer):
    class Meta:
        model = User
        fields = ('password', 'email')


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')


class FollowSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')


class FollowReadSerializer(serializers.ModelSerializer):
    following = CustomUserSerializer()

    class Meta:
        model = User
        fields = ('following',)
