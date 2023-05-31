from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    GenreTitle,
    Comment
)
from users.models import User


related_fields = ['category', 'genre_id', 'title_id', 'review_id', 'author']


def get_attrs(model, col_names, row):
    attrs = {}
    for i in col_names:
        if i == 'id':
            attrs[i] = int(row[i])
        if i not in related_fields:
            attrs[i] = row[i]
        else:
            if model is Title:
                attrs['category'] = Category.objects.get(
                    id=int(row['category'])
                )
            elif model is GenreTitle:
                attrs['title'] = Title.objects.get(
                    id=int(row['title_id'])
                )

                attrs['genre'] = Genre.objects.get(
                    id=int(row['genre_id'])
                )
            elif model is Review:
                attrs['title'] = Title.objects.get(
                    id=int(row['title_id'])
                )

                attrs['author'] = User.objects.get(
                    id=int(row['author'])
                )
            elif model is Comment:
                attrs['review'] = Review.objects.get(
                    id=int(row['review_id'])
                )

                attrs['author'] = User.objects.get(
                    id=int(row['author'])
                )
            else:
                pass
    return attrs
