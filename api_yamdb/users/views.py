from django.contrib.auth import tokens
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .pagination import UserListPagination
from .permissions import IsAdmin
from .serializers import (
    EditMyselfSerializer,
    SignUpSerialier,
    TokenCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet): # пермишн Admin
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    pagination_class = UserListPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    '''Получает код подтверждения на переданный email.'''
    serializer = SignUpSerialier(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        confirmation_code = tokens.default_token_generator.make_token(user)
        email = serializer.validated_data['email']
        send_mail(
            'Use confirmation code to sign up',
            f'Код подтверждения "{confirmation_code}".',
            'yamdb@team.com',
            [f'{email}'],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_create(request):
    '''Получает JWT-токен в обмен на username и confirmation code.'''
    serializer = TokenCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        if tokens.default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            access_token = RefreshToken.for_user(user).access_token
            return Response(
                {"token": str(access_token)}, status=status.HTTP_200_OK
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_miself(request):
    "Изменяет данные своей учетной записи."
    user = User.objects.get(username=request.user.username)
    if request.method == 'PATCH':
        serializer = EditMyselfSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = EditMyselfSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
