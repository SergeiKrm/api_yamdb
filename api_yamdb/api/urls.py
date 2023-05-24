from django.urls import include, path
from rest_framework import routers

from .views import (
    ReviewViewSet,
    CommentViewSet,
)


router_1 = routers.DefaultRouter()
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    # path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_1.urls)),
]
