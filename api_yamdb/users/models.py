from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    MAX_FIELD_LENGTH_254,
    MAX_FIELD_LENGTH_150,
    MAX_FIELD_LENGTH_50
)
from validators.validators import (
    characters_validator,
    username_not_me_validator
)


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
        max_length=MAX_FIELD_LENGTH_150,
        unique=True,
        blank=False,
        validators=[characters_validator, username_not_me_validator]
    )
    email = models.EmailField(
        max_length=MAX_FIELD_LENGTH_254,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=MAX_FIELD_LENGTH_150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_FIELD_LENGTH_150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=MAX_FIELD_LENGTH_50,
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
