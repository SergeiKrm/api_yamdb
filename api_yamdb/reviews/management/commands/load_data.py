import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    GenreTitle
)
from users.models import User
from reviews.utils import (
    get_attrs
)


MODELS = {
    'users': User,
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'review': Review,
    'comments': Comment,
}


class Command(BaseCommand):
    help = 'Creates database from csv files'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        # parser.add_argument('--model', type=str)

    def handle(self, *args, **kwargs):
        for name in MODELS.keys():
            file_name = os.path.join(os.path.join(
                kwargs['path'], name + '.csv'
            ))
            model = MODELS[name]
            model.objects.all().delete()

            with open(file_name, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cols = reader.fieldnames
                for row in reader:
                    attrs = get_attrs(
                        model,
                        cols,
                        row
                    )

                    if not model.objects.filter(**attrs).exists():
                        instance = model.objects.create(
                            **attrs
                        )
                        instance.save()
