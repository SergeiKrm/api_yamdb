from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from users.models import User


related_fields = {
    'category': Category,
    'genre_id': Genre,
    'title_id': Title,
    'review_id': Review,
    'author': User
}


def get_model_instance_params(col_names, row):
    attrs = {}
    for i in col_names:
        if i == 'id':
            attrs[i] = int(row[i])
        elif i not in related_fields:
            attrs[i] = row[i]
        else:
            model = related_fields[i]
            try:
                attrs[i.replace('_id', '')] = model.objects.get(
                    id=int(row[i])
                )
            except model.DoesNotExist:
                attrs[i.replace('_id', '')] = None
    return attrs
