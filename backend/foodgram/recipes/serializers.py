import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe,
                            TagRecipe, IngredientAmount,
                            RecipeIngredientAmount)
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    author = CustomUserSerializer(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            TagRecipe.objects.create(
                tag=tag, recipe=recipe
            )

        for ingredient in ingredients:
            ingt = Ingredient.objects.get(id=ingredient['ingredient'].id)
            ingrt_amount = IngredientAmount.objects.create(
                ingredient=ingt, amount=ingredient['amount']
            )
            RecipeIngredientAmount.objects.create(
                recipe=recipe, ingredientamount=ingrt_amount
            )

        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')

        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        tag_lst, ingt_amount_lst = [], []

        recipe = Recipe.objects.get(id=instance.id)

        for tag in tags_data:
            current_tag = Tag.objects.get(pk=tag.pk)
            tag_lst.append(current_tag)

        for ingredient in ingredients_data:
            ingt = Ingredient.objects.get(id=ingredient['ingredient'].id)
            ingt_amount, _ = IngredientAmount.objects.get_or_create(
                ingredient=ingt, amount=ingredient['amount']
            )
            RecipeIngredientAmount.objects.get_or_create(
                recipe=recipe, ingredientamount=ingt_amount)
            ingt_amount_lst.append(ingt_amount)

        instance.tags.set(tag_lst)
        instance.ingredients.set(ingt_amount_lst)

        instance.save()

        return instance
