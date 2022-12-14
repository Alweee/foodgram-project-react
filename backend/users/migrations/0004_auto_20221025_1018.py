# Generated by Django 3.2.15 on 2022-10-25 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221022_1300'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_user_author',
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='unique_subscriber_author'),
        ),
    ]
