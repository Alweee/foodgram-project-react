from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
from users.views import FollowingList, SubscribeApiView

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', FollowingList.as_view()),
    path('users/<int:id>/subscribe/', SubscribeApiView.as_view())
]
