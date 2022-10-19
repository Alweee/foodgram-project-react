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
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')

    # def get_is_subscribed(self, obj):
    #     current_user = self.context['request'].user
    #     return Subscription.objects.filter(
    #         user=current_user,
    #         author=obj).exists()


class SubscribeReadSerializer(serializers.ModelSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')

    # def get_is_subscribed(self, obj):
    #     current_user = self.context['request'].user
    #     return Subscription.objects.filter(
    #         user=current_user,
    #         author=obj).exists()


class SubscribeSerializer(CustomUserSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')
