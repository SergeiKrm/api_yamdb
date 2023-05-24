# import csv
# from django.core.management.base import BaseCommand
# from reviews.models import Title, Review, Comment


# MODELS = {
#     'Title': Title,
#     'Review': Review,
#     'Comment': Comment,
# }


# class Command(BaseCommand):
#     help = 'Creates database from csv files'

#     def add_arguments(self, parser):
#         parser.add_argument('--path', type=str)
#         parser.add_argument('--model', type=str)

#     def handle(self, *args, **kwargs):
#         path = kwargs['path']
#         model_name = kwargs['model']
#         model = MODELS[model_name]
#         fields = [f.name for f in model._meta.get_fields()]

#         with open(path, 'rt') as f:
#             reader = csv.reader(f, dialect='excel')
#             for row in reader:
#                 attrs = {}
#                 for i in range(len(fields)):
#                     attrs[fields[i]]: row[i]

#                 instance = model.objects.create(
#                     **attrs
#                 )
#                 instance.save()
