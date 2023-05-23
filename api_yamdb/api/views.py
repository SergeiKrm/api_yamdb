from django.shortcuts import get_object_or_404
from rest_framework import viewsets


from reviews.models import Title, Review
from .serializers import (
    ReviewSerializer,
    CommentSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes

    def get_post(self, id):
        return get_object_or_404(Title, id=id)

    def get_queryset(self):
        return self.get_post(
            self.kwargs.get('title_id')
        ).reviews

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.get_post(self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes

    def get_post(self, id):
        return get_object_or_404(Review, id=id)

    def get_queryset(self):
        return self.get_post(
            self.kwargs.get('review_id')
        ).comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.get_post(self.kwargs.get('review_id'))
        )
