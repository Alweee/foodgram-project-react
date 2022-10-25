from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Tag, Ingredient, Recipe, Favorite
from recipes.serializers import (TagSerializer, IngredientSerializer,
                                 RecipeSerializer, RecipeReadSerializer,
                                 FavoriteSerializer)


class ListTags(APIView):
    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveTag(APIView):
    def get(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListIngredients(APIView):
    def get(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveIngredient(APIView):
    def get(self, request, pk):
        ingredient = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(
            ingredient,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRecipe(APIView):
    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = Recipe.objects.all()
        serializer = RecipeReadSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRecipeDetail(APIView):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeReadSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(
            recipe,
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiFavorite(APIView):
    def post(self, request, pk):
        current_recipe = Recipe.objects.get(pk=pk)
        Favorite.objects.create(
            recipe=current_recipe,
            user=request.user
        )
        serializer = FavoriteSerializer(
            current_recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        current_recipe = Recipe.objects.get(pk=pk)
        favorite = Favorite.objects.get(
            recipe=current_recipe,
            user=request.user
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiShoppingCart(APIView):
    def post(self, request, pk):
        current_recipe =

    def delete(self, request, pk):
        pass


class ApiDownloadShoppingCart(APIView):
    def get(self, request):
        pass
