from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)
from recipes.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeReadSerializer,
)
from recipes.permissions import OnlyAuthor
from users.serializers import RecipeInfoSerializer
from users.pagination import CustomPageNumberPagination


class TagList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags,
            many=True,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class TagDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        current_tag = get_object_or_404(Tag, pk=pk)

        serializer = TagSerializer(
            current_tag,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ingredients = Ingredient.objects.all()

        name = self.request.query_params.get('search')
        if name is not None:
            ingredients = ingredients.filter(name__startswith=name)

        serializer = IngredientSerializer(
            ingredients,
            many=True,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)

        serializer = IngredientSerializer(
            ingredient,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRecipe(APIView, CustomPageNumberPagination):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request})

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        recipes = Recipe.objects.all()

        is_favorited = request.query_params.get('is_favorited')
        if is_favorited is not None:
            is_favorited = int(is_favorited)
            favorite_recipes = Favorite.objects.values_list(
                'recipe',
                flat=True
            )
            if is_favorited == 1:
                recipes = recipes.filter(id__in=favorite_recipes)

        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart is not None:
            is_in_shopping_cart = int(is_in_shopping_cart)
            shopping_cart_recipes = ShoppingCart.objects.values_list(
                'recipe',
                flat=True
            )
            if is_in_shopping_cart == 1:
                recipes = recipes.filter(id__in=shopping_cart_recipes)

        author = request.query_params.get('author')
        if author is not None:
            author = int(author)
            recipes = recipes.filter(author_id=author)

        tags = self.request.query_params.getlist('tags')
        if tags is not None:
            recipes = recipes.filter(tags__slug__in=tags).distinct()

        results = self.paginate_queryset(recipes, request, view=self)

        serializer = RecipeReadSerializer(
            results,
            many=True,
            context={'request': request})

        return self.get_paginated_response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)
        return super().get_permissions()


class ApiRecipeDetail(APIView):
    permission_classes = [OnlyAuthor]

    def get(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        serializer = RecipeReadSerializer(
            current_recipe,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        serializer = RecipeSerializer(
            current_recipe,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)
        current_recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)
        return super().get_permissions()


class ApiFavorite(APIView):
    def post(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        try:
            Favorite.objects.create(
                recipe=current_recipe,
                user=request.user)
        except IntegrityError:
            return Response(
                {'errors': 'Recipe already is in favorite'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = RecipeInfoSerializer(
            current_recipe,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        try:
            favorite = Favorite.objects.get(
                recipe=current_recipe,
                user=request.user)
        except ObjectDoesNotExist:
            return Response(
                {'errors': 'Recipe not found in favorite'},
                status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiShoppingCart(APIView):
    def post(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        try:
            ShoppingCart.objects.create(
                user=request.user,
                recipe=current_recipe)

        except IntegrityError:
            return Response(
                {'errors': 'Recipe already is in shopping cart'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = RecipeInfoSerializer(
            current_recipe,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        try:
            shoppingcart = ShoppingCart.objects.get(
                user=request.user,
                recipe=current_recipe
            )
        except ObjectDoesNotExist:
            return Response({'error': 'Recipe not found in shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)
        shoppingcart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    file_path = (f'{settings.MEDIA_ROOT}\\'
                 f'user_{request.user.username}\\'
                 f'shopping_cart.txt')

    shoppingcart = ShoppingCart.objects.filter(user=request.user)

    data = {}

    for purchase in shoppingcart:
        ingredients = purchase.recipe.ingredients.all()

        for ingredient in ingredients:
            recipeingredient = RecipeIngredient.objects.get(
                recipe=purchase.recipe,
                ingredient=ingredient
            )
            if ingredient.name in data.keys():
                data[ingredient.name] += recipeingredient.amount
            else:
                data[ingredient.name] = recipeingredient.amount

    with open(file_path, 'w') as file:
        for name in data.keys():
            ingredient = Ingredient.objects.get(name=name)
            file.write(f'{name} '
                       f'({ingredient.measurement_unit}) - '
                       f'{data[name]}\n')

    FilePointer = open(file_path, 'r')
    response = HttpResponse(FilePointer, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=shopping_cart.txt'

    return response
