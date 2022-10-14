from django.db import models

from users.models import User
from recipes.utils import user_directory_path


class Amount(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return self.amount


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    measurement_unit = models.CharField(max_length=100)
    amount = models.ManyToManyField(
        Amount,
        through='IngredientAmount',
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


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
        IngredientAmount
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    cooking_time = models.IntegerField()


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient.name} {self.recipe.name}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag.name} {self.recipe.name}'
