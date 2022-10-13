from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (TagSerializer, IngredientSerializer,
                                 RecipeSerializer, RecipeReadSerializer)


class ListTags(APIView):
    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveTag(APIView):
    def get(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListIngredients(APIView):
    def get(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveIngredient(APIView):
    def get(self, request, pk):
        ingredient = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRecipe(APIView):
    def post(self, request):
        serializer = RecipeSerializer(request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = Recipe.objects.all()
        serializer = RecipeReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
