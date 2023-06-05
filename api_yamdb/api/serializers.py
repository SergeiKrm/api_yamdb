from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import MAX_FIELD_LENGTH_254, MAX_FIELD_LENGTH_150
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.models import User
from validators.validators import (
    characters_validator,
    username_not_me_validator
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = TitleSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = get_object_or_404(
                Title,
                id=self.context['view'].kwargs['title_id']
            )
            if Review.objects.filter(
                author=author,
                title=title
            ).exists():
                raise serializers.ValidationError(
                    'Допускается не более одного отзыва от одного автора!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = ReviewSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_FIELD_LENGTH_150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            characters_validator,
            username_not_me_validator
        ]
    )
    email = serializers.EmailField(
        max_length=MAX_FIELD_LENGTH_254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerialier(UserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class EditMyselfSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_FIELD_LENGTH_150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            characters_validator,
            username_not_me_validator
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
