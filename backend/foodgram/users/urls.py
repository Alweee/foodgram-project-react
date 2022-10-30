from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.views import (
    CustomUserViewSet,
    SubscriptionList,
    ApiSubscription
)

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionList.as_view()),
    path('users/<int:pk>/subscribe/', ApiSubscription.as_view()),
]

urlpatterns += [
    path('', include(router_v1.urls)),
]
