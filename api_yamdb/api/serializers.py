from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.generics import get_object_or_404

from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    Comment
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
