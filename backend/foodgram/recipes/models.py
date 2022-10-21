from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from recipes.utils import user_directory_path


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Tag name'
    )
    color = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Tag color',
        help_text='String in HEX format'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Tag slug'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Ingredient  measurement_unit',
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='recipe author'
    )
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='recipe name'
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='recipe image'
    )
    text = models.TextField(
        verbose_name='recipe description'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='recipe ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='recipe tags'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'min cooking time in minutes'),
            MaxValueValidator(1440, 'max cooking time in minutes')
        ],
        verbose_name='cooking_time in minutes'
    )

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='recipe tag'
    )

    class Meta:
        verbose_name_plural = 'recipe tags'

    def __str__(self):
        return f'{self.recipe} | {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='recipe ingredient'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1, 'min amount'),
            MaxValueValidator(10000, 'max amount')
        ],
        verbose_name='ingredient amount'
    )

    class Meta:
        verbose_name_plural = 'recipe ingredients'

    def __str__(self):
        return f'{self.recipe} | {self.ingredient} | {self.amount}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name_plural = 'favorites'

    def __str__(self):
        return f'{self.recipe} | {self.user}'
