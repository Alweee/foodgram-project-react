from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet

from rest_framework import permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.pagination import CustomPagination
from users.models import User, Subscription
from users.serializers import CustomUserSerializer, SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class SubscriptionList(APIView):
    def get(self, request):
        queryset = User.objects.filter(following__subscriber=request.user)
        serializer = SubscribeSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionApiView(APIView):
    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        sub = Subscription.objects.create(
            subscriber=request.user,
            author=author)
        serializer = SubscribeSerializer(
            sub.author,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        subscription = Subscription.objects.get(
            subscriber=request.user,
            author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
