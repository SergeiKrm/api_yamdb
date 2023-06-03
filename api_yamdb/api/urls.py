# from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    edit_myself,
    sign_up,
    token_create
)


router_1 = routers.DefaultRouter()
router_1.register(r'genres', GenreViewSet, basename='genres')
router_1.register(r'categories', CategoryViewSet, basename='categories')
router_1.register(r'titles', TitleViewSet, basename='titles')
router_1.register('users', UserViewSet)
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

auth_urls = [
    path('auth/signup/', sign_up, name='signup'),
    path('auth/token/', token_create, name='token_craete'),
]

urlpatterns = [
    path('users/me/', edit_myself, name='edit_myself'),
    path('', include(router_1.urls)),
    path('', include(auth_urls)),
]
