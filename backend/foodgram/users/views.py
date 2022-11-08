from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from djoser.views import UserViewSet

from users.pagination import CustomPageNumberPagination
from users.models import User, Subscription
from users.serializers import CustomUserSerializer, SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class SubscriptionList(APIView, CustomPageNumberPagination):
    def get(self, request):
        authors = User.objects.filter(authors__subscriber=request.user)
        results = self.paginate_queryset(authors, request, view=self)

        serializer = SubscribeSerializer(
            results,
            many=True,
            context={'request': request})

        return self.get_paginated_response(serializer.data)


class ApiSubscription(APIView):
    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if author == self.request.user:
            return Response({'errors': 'You can\'t subscribe to yourself'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscription.objects.create(
                subscriber=request.user,
                author=author)
        except IntegrityError:
            return Response(
                {'errors': 'You can\'t subscribe to the author twice'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = SubscribeSerializer(
            subscription.author,
            context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)

        try:
            subscription = Subscription.objects.get(
                subscriber=request.user,
                author=author)
            subscription.delete()
        except ObjectDoesNotExist:
            return Response({'errors': 'You weren\'t subscribed to this user'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
