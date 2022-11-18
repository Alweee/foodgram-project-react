from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    ApiFavorite,
    ApiRecipe,
    ApiRecipeDetail,
    ApiShoppingCart,
    ApiSubscription,
    CustomUserViewSet,
    download_shopping_cart,
    IngredientDetail,
    IngredientList,
    TagDetail,
    TagList,
    SubscriptionList,
)

recipes_urls = [
    path('tags/', TagList.as_view()),
    path('tags/<int:pk>/', TagDetail.as_view()),
    path('ingredients/', IngredientList.as_view()),
    path('ingredients/<int:pk>/', IngredientDetail.as_view()),
    path('recipes/', ApiRecipe.as_view()),
    path('recipes/<int:pk>/', ApiRecipeDetail.as_view()),
    path('recipes/<int:pk>/favorite/', ApiFavorite.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ApiShoppingCart.as_view()),
    path('recipes/download_shopping_cart/',
         download_shopping_cart,
         name='shopping_cart'),
]

users_urls = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionList.as_view()),
    path('users/<int:pk>/subscribe/', ApiSubscription.as_view()),
]

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet)

router_v1_urls = [
    path('', include(router_v1.urls)),
]

urlpatterns = recipes_urls + users_urls + router_v1_urls
