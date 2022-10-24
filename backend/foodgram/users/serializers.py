from djoser.serializers import (UserCreateSerializer, TokenCreateSerializer,
                                UserSerializer)

from rest_framework import serializers

from users.models import User, Subscription
from recipes.models import Recipe


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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        return Subscription.objects.filter(
            subscriber=current_user,
            author=obj).exists()


class RecipeReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeReadSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        recipe_count = Recipe.objects.filter(author=obj).count()
        return recipe_count

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        return Subscription.objects.filter(
            user=current_user,
            author=obj).exists()
