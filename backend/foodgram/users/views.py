from djoser.views import UserViewSet
from models import User


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
