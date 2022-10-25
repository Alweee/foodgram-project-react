import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe, RecipeTag,
                            RecipeIngredient, Favorite)

from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'author',
                  'image', 'name', 'text', 'cooking_time')
        read_only_fields = ('author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            RecipeTag.objects.create(
                tag=tag, recipe=recipe
            )

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=ingredient['id'].id
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )

        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        tags_lst, ingredients_lst = [], []

        for tag in tags:
            current_tag = Tag.objects.get(id=tag.id)
            tags_lst.append(current_tag)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'].id)
            RecipeIngredient.objects.get_or_create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )
            ingredients_lst.append(current_ingredient.id)

        instance.tags.set(tags_lst)
        instance.ingredients.set(ingredients_lst)

        instance.save()

        return instance

    def to_representation(self, instance):
        request = self.context['request']
        serializer = RecipeReadSerializer(
            instance,
            context={'request': request}
        )
        return serializer.data


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('__all__',)

    def get_author(self, obj):
        request = self.context['request']
        serializer = CustomUserSerializer(
            obj.author,
            context={'request': request}
        )
        return serializer.data

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        serializer = RecipeIngredientReadSerializer(queryset, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        return Favorite.objects.filter(
            user=current_user,
            recipe=obj
        ).exists()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
