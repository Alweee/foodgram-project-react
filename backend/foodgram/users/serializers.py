from rest_framework import serializers

from djoser.serializers import (UserCreateSerializer, TokenCreateSerializer,
                                UserSerializer)
from users.models import User


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
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class UserSubscribeSerializer(UserSerializer):
    # recipes = RecipeSerializer()
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
