from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import characters_validator


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = [
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[characters_validator]
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
        choices=ROLES,
        default='user'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'

    def __str__(self):
        return (self.get_full_name()
                if (self.first_name and self.last_name) else self.username)
