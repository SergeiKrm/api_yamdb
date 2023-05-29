from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import UserViewSet, sign_up, token_create, edit_miself

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)

urlpatterns = [
    path('users/me/', edit_miself, name='edit_myself'),
    path('', include(router_v1.urls)),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # !!
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/', TokenVerifyView.as_view(), name='token_verify'),  # !!
    
    path('auth/signup/', sign_up, name='signup'),
    path('auth/token/', token_create, name='token_craete'),
]
