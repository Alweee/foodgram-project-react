from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet

from rest_framework import permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.pagination import CustomPagination
from users.models import User, Subscription
from users.serializers import (CustomUserSerializer, UserSubscribeSerializer,
                               FollowListSerializer)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        return User.objects.all()


class FollowingList(APIView):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        queryset = user.follower.all()
        serializer = FollowListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeApiView(APIView):
    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        serializer = UserSubscribeSerializer(author)
        Subscription.objects.create(user=request.user, following=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subscription = Subscription.objects.get(
            user=request.user,
            following=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
