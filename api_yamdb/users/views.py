from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import User
from .serializers import SignUpSerialier, UserSerializer


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
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        email = serializer.validated_data['email']
        confirmation_code = user._generate_jwt_token
        send_mail(
            'Confirmation code',
            f'Confirmation code {confirmation_code}.',
            'yamdb@team.com',
            [f'{email}'],  #  "Кому"
            fail_silently=False, # Сообщать об ошибках)
        )   
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
