from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Tag, Ingredient, Recipe


class ListRetrieveTags(APIView):
    pass
