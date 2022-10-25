from django.urls import path

from recipes.views import (ListTags, RetrieveTag, ListIngredients,
                           RetrieveIngredient, ApiRecipe, ApiRecipeDetail,
                           ApiFavorite, ApiShoppingCart,
                           download_shopping_cart)


urlpatterns = [
    path('tags/', ListTags.as_view()),
    path('tags/<int:pk>/', RetrieveTag.as_view()),
    path('ingredients/', ListIngredients.as_view()),
    path('ingredients/<int:pk>/', RetrieveIngredient.as_view()),
    path('recipes/', ApiRecipe.as_view()),
    path('recipes/<int:pk>/', ApiRecipeDetail.as_view()),
    path('recipes/<int:pk>/favorite/', ApiFavorite.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ApiShoppingCart.as_view()),
    path('recipes/download_shopping_cart/',
         download_shopping_cart,
         name='shopping_cart'),
]
