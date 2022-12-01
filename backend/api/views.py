from pathlib import Path

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet

from rest_framework import status, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPageNumberPagination
from api.permissions import OnlyAuthor
from api.serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    RecipeInfoSerializer,
    RecipeReadSerializer,
    RecipeSerializer,
    SubscriptionSerializer,
    TagSerializer
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)
from users.models import Subscription, User


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
        name = self.request.query_params.get('name')
        if name is not None:
            ingredients = Ingredient.objects.filter(name__startswith=name)
        else:
            ingredients = Ingredient.objects.all()

        serializer = IngredientSerializer(
            ingredients,
            many=True,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        current_ingredient = get_object_or_404(Ingredient, pk=pk)

        serializer = IngredientSerializer(
            current_ingredient,
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
                flat=True)
            if is_favorited == 1:
                recipes = recipes.filter(id__in=favorite_recipes)

        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart is not None:
            is_in_shopping_cart = int(is_in_shopping_cart)
            shopping_cart_recipes = ShoppingCart.objects.values_list(
                'recipe',
                flat=True)
            if is_in_shopping_cart == 1:
                recipes = recipes.filter(id__in=shopping_cart_recipes)

        author = request.query_params.get('author')
        if author is not None:
            author = int(author)
            recipes = recipes.filter(author_id=author)

        tags = self.request.query_params.getlist('tags')
        if len(tags):
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
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)

        serializer = RecipeReadSerializer(
            current_recipe,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)
        self.check_object_permissions(request, current_recipe)

        serializer = RecipeSerializer(
            current_recipe,
            data=request.data,
            context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        current_recipe = get_object_or_404(Recipe, pk=pk)
        self.check_object_permissions(request, current_recipe)
        current_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return (OnlyAuthor(),)
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
            favorite.delete()

        except ObjectDoesNotExist:
            return Response(
                {'errors': 'Recipe not found in favorite'},
                status=status.HTTP_400_BAD_REQUEST)

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
                recipe=current_recipe)
            shoppingcart.delete()

        except ObjectDoesNotExist:
            return Response({'error': 'Recipe not found in shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    file_path = Path(settings.MEDIA_ROOT,
                     'user_'+request.user.username,
                     'shopping_cart.txt')

    user_shopping_cart = RecipeIngredient.objects.select_related(
            'recipe', 'ingredient').filter(
        recipe__shoppingcarts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount')
    all_count_ingredients = user_shopping_cart.values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
            total=Sum('amount')).order_by('-total')

    with open(file_path, 'w', encoding='utf-8') as file:
        for ingredient in all_count_ingredients:
            file.write(
                f'{ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) - '
                f'{ingredient["total"]}\n')

    FilePointer = open(file_path, 'r', encoding='utf-8')
    response = HttpResponse(FilePointer, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=shopping_cart.txt'

    return response


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class SubscriptionList(APIView, CustomPageNumberPagination):
    def get(self, request):
        authors = User.objects.filter(authors__subscriber=request.user)
        results = self.paginate_queryset(authors, request, view=self)

        serializer = SubscriptionSerializer(
            results,
            many=True,
            context={'request': request})

        return self.get_paginated_response(serializer.data)


class ApiSubscription(APIView):
    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if author == self.request.user:
            return Response({'errors': 'You can\'t subscribe to yourself'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscription.objects.create(
                subscriber=request.user,
                author=author)

        except IntegrityError:
            return Response(
                {'errors': 'You can\'t subscribe to the author twice'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = SubscriptionSerializer(
            subscription.author,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)

        try:
            subscription = Subscription.objects.get(
                subscriber=request.user,
                author=author)
            subscription.delete()

        except ObjectDoesNotExist:
            return Response(
                {'errors': 'You weren\'t subscribed to this user'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
