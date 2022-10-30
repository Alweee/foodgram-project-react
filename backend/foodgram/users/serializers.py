from rest_framework import serializers

from djoser.serializers import (
    UserCreateSerializer,
    TokenCreateSerializer,
    UserSerializer
)

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
        auth = self.context['request'].auth
        if not auth:
            return False
        return Subscription.objects.filter(
            subscriber=current_user,
            author=obj
        ).exists()


class RecipeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('recipes',)

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user

        return Subscription.objects.filter(
            subscriber=current_user,
            author=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)

        if recipes_limit is not None:
            recipes = recipes[:int(recipes_limit)]

        serializer = RecipeInfoSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        recipe_count = Recipe.objects.filter(author=obj).count()
        return recipe_count
