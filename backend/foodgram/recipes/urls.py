from django.urls import path

from recipes.views import (ListTags, RetrieveTag, ListIngredients,
                           RetrieveIngredient, ApiRecipe)


urlpatterns = [
    path('tags/', ListTags.as_view()),
    path('tags/<int:pk>/', RetrieveTag.as_view()),
    path('ingredients/', ListIngredients.as_view()),
    path('ingredients/<int:pk>/', RetrieveIngredient.as_view()),
    path('recipes/', ApiRecipe.as_view()),
]
