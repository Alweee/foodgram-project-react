from djoser.views import UserViewSet
from rest_framework import permissions, filters

from users.pagination import CustomPagination
from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
