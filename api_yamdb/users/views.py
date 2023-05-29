from django.contrib.auth import tokens
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    EditMyselfSerializer,
    SignUpSerialier,
    TokenCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(['POST'])  # пермишн Any прилепить
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
            [f'{email}'],  # "Кому"
            fail_silently=False,  # Сообщать об ошибках
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])  # пермишн Any прилепить
def token_create(request):
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
def edit_miself(request):   # пермишн только на владельца учётки
    "Изменяет данные своей учетной записи."
    user = User.objects.get(username=request.user.username)
    
    if request.method == 'PATCH':
        serializer = EditMyselfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = EditMyselfSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
