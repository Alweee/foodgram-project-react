# Generated by Django 3.2.15 on 2022-10-18 09:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Ingredient name')),
                ('measurement_unit', models.CharField(max_length=50, verbose_name='Ingredient  measurement_unit')),
            ],
            options={
                'verbose_name_plural': 'ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='recipe name')),
                ('image', models.ImageField(upload_to=recipes.utils.user_directory_path, verbose_name='recipe image')),
                ('text', models.TextField(verbose_name='recipe description')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'min cooking time in minutes'), django.core.validators.MaxValueValidator(1440, 'max cooking time in minutes')], verbose_name='cooking_time in minutes')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'recipes',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Tag name')),
                ('color', models.CharField(help_text='String in HEX format', max_length=30, unique=True, verbose_name='Tag color')),
                ('slug', models.SlugField(unique=True, verbose_name='Tag slug')),
            ],
            options={
                'verbose_name_plural': 'tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='recipe object')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag', verbose_name='recipe tag')),
            ],
            options={
                'verbose_name_plural': 'recipe tags',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'min amount'), django.core.validators.MaxValueValidator(10000, 'max amount')], verbose_name='ingredient amount')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='recipe ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='recipe object')),
            ],
            options={
                'verbose_name_plural': 'recipe ingredients',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='recipe ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.RecipeTag', to='recipes.Tag', verbose_name='recipe tags'),
        ),
    ]
