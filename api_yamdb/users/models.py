from django.contrib.auth.models import AbstractUser
from django.db import models


# Расширяю модель пользователя.
class User(AbstractUser):

    Roles = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    # переопределяю поле "email", т.к. в базовой модели это поле
    # не уникальное и не обязательное.
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
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
