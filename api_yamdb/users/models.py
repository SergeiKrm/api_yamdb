from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    Roles = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        blank=False,
        choices=Roles,
        default='user'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'

    def __str__(self):
        if self.first_name and self.last_name:
            full_name = self.get_full_name()
            return full_name
        return self.username
