from django.contrib.auth import tokens
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .pagination import UserListPagination
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    EditMyselfSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerialier,
    TitleSerializer,
    TokenCreateSerializer,
    UserSerializer,
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_title(self, id):
        return get_object_or_404(
            Title, id=id
        )

    def get_queryset(self):
        return self.get_title(self.kwargs.get('title_id')).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_review(self, id):
        return get_object_or_404(
            Review, id=id
        )

    def get_queryset(self):
        return self.get_review(self.kwargs.get('review_id')).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(self.kwargs.get('review_id'))
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    pagination_class = UserListPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    '''Получает код подтверждения на переданный email.'''
    user = User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email'))
    if not user.exists():
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
    confirmation_code = tokens.default_token_generator.make_token(user[0])
    email = user[0].email
    send_mail(
        'Use confirmation code to sign up',
        f'Код подтверждения "{confirmation_code}".',
        'yamdb@team.com',
        [f'{email}'],
        fail_silently=False,
    )
    return Response(request.data, status=status.HTTP_200_OK)


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
