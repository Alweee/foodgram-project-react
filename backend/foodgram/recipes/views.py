from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions

from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient,
                            Favorite, ShoppingCart,)

from recipes.serializers import (TagSerializer, IngredientSerializer,
                                 RecipeSerializer, RecipeReadSerializer,
                                 FavoriteSerializer, ShoppingCartSerializer)


class TagList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        current_tag = get_object_or_404(Tag, pk=pk)

        serializer = TagSerializer(
            current_tag,
            context={'request': request}
        )
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
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)

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
        recipes = Recipe.objects.all()

        serializer = RecipeReadSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRecipeDetail(APIView):
    def get(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        serializer = RecipeReadSerializer(
            current_recipe,
            context={'request': request}
        )
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


class ApiFavorite(APIView):
    def post(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        favorite = Favorite.objects.create(
            recipe=current_recipe,
            user=request.user
        )
        serializer = FavoriteSerializer(
            favorite,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        favorite = Favorite.objects.get(
            recipe=current_recipe,
            user=request.user
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiShoppingCart(APIView):
    def post(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        ShoppingCart.objects.create(
            user=request.user,
            recipe=current_recipe
        )
        serializer = ShoppingCartSerializer(
            current_recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        shoppingcart = ShoppingCart.objects.get(
            user=request.user,
            recipe=current_recipe
        )
        shoppingcart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    file_path = (f'{settings.MEDIA_ROOT}\\'
                 f'user_{request.user.username}\\'
                 f'shopping_cart.txt')

    shoppingcart = ShoppingCart.objects.filter(user=request.user)

    data = {}

    with open(file_path, 'w') as file:
        for obj in shoppingcart:
            ingredients = obj.recipe.ingredients.all()

            for ingredient in ingredients:
                recipeingredient = RecipeIngredient.objects.get(
                    recipe=obj.recipe,
                    ingredient=ingredient
                )
                if ingredient.name in data.keys():
                    data[ingredient.name] += recipeingredient.amount
                else:
                    data[ingredient.name] = recipeingredient.amount

                file.write(f'{ingredient.name} '
                           f'({ingredient.measurement_unit}) - '
                           f'{recipeingredient.amount}\n')

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
