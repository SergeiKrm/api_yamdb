from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_1 = routers.DefaultRouter()
router_1.register(r'genres', GenreViewSet, basename='genres')
router_1.register(r'categories', CategoryViewSet, basename='categories')
router_1.register(r'titles', TitleViewSet, basename='titles')
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    # path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_1.urls)),
]
