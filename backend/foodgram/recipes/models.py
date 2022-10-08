from django.db import models

from users.models import User
from recipes.utils import user_directory_path


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
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
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=user_directory_path)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    cooking_time = models.IntegerField()


class IngredientRecipe(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient_id.name} {self.recipe_id.name}'


class TagRecipe(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag_id.name} {self.recipe_id.name}'
