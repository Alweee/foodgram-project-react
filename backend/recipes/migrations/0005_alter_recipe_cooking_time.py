# Generated by Django 3.2.15 on 2022-12-06 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(verbose_name='Время приготовления в минутах'),
        ),
    ]