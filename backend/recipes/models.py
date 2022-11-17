from django.core.validators import MinValueValidator
from django.db import models

from recipes.utils import user_directory_path
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Цвет тега',
        help_text='Цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug тега',
        help_text='Человеко-понятный уникальный идентификатор'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения ингредиента',
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name='Изображение рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'minimum cooking time in minutes'),
        ],
        verbose_name='Время приготовления в минутах'
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('recipe__name',)

    def __str__(self):
        return f'{self.recipe.name} c тегом {self.tag.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1, 'min amount')
        ],
        verbose_name='Колличество ингредиента'
    )

    class Meta:
        ordering = ('recipe__name',)

    def __str__(self):
        return f'{self.recipe}->{self.ingredient}->{self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('recipe__name',)
        verbose_name_plural = 'Избранные'
        default_related_name = '%(class)ss'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniquee_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user}->{self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcarts'
    )

    class Meta:
        ordering = ('recipe__name',)
        default_related_name = '%(class)ss'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user}->{self.recipe}'
