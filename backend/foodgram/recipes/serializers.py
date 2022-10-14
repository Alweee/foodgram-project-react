import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe,
                            TagRecipe, IngredientRecipe)
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class Ingredient2Serializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=1)  # тут закончил

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')

    def get_amount(self, object):
        return


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = Ingredient2Serializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            TagRecipe.objects.create(
                tag=tag, recipe=recipe
            )
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient=ingredient, recipe=recipe  # тут ошибка
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data('cooking_time',
                                               instance.cooking_time)

        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        taglst, inglst = [], []
        for tag in tags_data:
            current_tag = Tag.objects.get(pk=tag.pk)
            taglst.append(current_tag)
        for ingredient in ingredients_data:
            current_ingredient = Ingredient.objects.get(**ingredient)
            inglst.append(current_ingredient)
        instance.tags.set(taglst)
        instance.ingredients.set(inglst)
        instance.save()
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = CustomUserSerializer()
    ingredients = Ingredient2Serializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')
