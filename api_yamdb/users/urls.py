from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, sign_up, token_create, edit_miself


router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)

urlpatterns = [
    path('users/me/', edit_miself, name='edit_myself'),
    path('', include(router_v1.urls)),
    path('auth/signup/', sign_up, name='signup'),
    path('auth/token/', token_create, name='token_craete'),
]
