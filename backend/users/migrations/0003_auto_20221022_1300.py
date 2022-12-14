# Generated by Django 3.2.15 on 2022-10-22 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_rename_user_subscription_subscriber'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_user_author',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='author',
            field=models.ForeignKey(help_text='the user that others subscribe to', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='unique_user_author'),
        ),
    ]
