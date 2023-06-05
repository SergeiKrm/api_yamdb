from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from users.models import User


art_piece_characteristic = {
    'category': Category,
    'genre_id': Genre,
    'title_id': Title,
    'review_id': Review,
    'author': User
}


def get_model_instance_params(column_names, row):
    attrs = {}
    for column_name in column_names:
        if column_name == 'id':
            attrs[column_name] = int(row[column_name])
        elif column_name not in art_piece_characteristic:
            attrs[column_name] = row[column_name]
        else:
            model = art_piece_characteristic[column_name]
            try:
                attrs[column_name.replace('_id', '')] = model.objects.get(
                    id=int(row[column_name])
                )
            except model.DoesNotExist:
                attrs[column_name.replace('_id', '')] = None
    return attrs
