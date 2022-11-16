from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        help_text='the user that others subscribe to'
    )

    def __str__(self):
        return f'{self.subscriber} to {self.author}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscriber_author'
            )
        ]
        verbose_name_plural = 'subscriptions'
