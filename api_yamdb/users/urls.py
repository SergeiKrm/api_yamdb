from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import UserViewSet, sign_up

router = DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # !!
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenVerifyView.as_view(), name='token_verify'),  # !!
    path('auth/signup/', sign_up, name='signup'),
]
