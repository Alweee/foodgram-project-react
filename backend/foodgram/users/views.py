from djoser.views import UserViewSet

from rest_framework import permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.pagination import CustomPagination
from users.models import User
from users.serializers import CustomUserSerializer, UserSubscribeSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class FollowingList(APIView):
    def get(self, request):
        followings = request.user.following.all()
        serializer = UserSubscribeSerializer(followings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
