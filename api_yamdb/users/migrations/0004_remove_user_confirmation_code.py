# Generated by Django 3.2 on 2023-05-29 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]
