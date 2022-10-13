from django.urls import path

from recipes.views import (ListRetrieveTags, ListRetrieveIngredients,
                           ApiRecipe, ApiRecipeDetail)


urlpatterns = [
    path('tags/', ListRetrieveTags.as_view()),
    path('ingredients/', ListRetrieveIngredients.as_view()),
    path('recipes/', ApiRecipe.as_view()),
    path('recipes/<int:pk>/', ApiRecipeDetail.as_view())
]
