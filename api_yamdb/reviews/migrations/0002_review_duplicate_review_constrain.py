# Generated by Django 3.2 on 2023-05-30 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title_id', 'author'), name='duplicate_review_constrain'),
        ),
    ]