from django.db import models

from users.models import User
from recipes.utils import user_directory_path

class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    amount = models.IntegerField()
    measurement_unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=user_directory_path)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        trough='IngredientRecipe'
    )
    tags = models.
