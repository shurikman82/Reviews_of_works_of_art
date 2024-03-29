import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, permissions,
                            status, viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from api_yamdb.settings import ADMIN_EMAIL
from .filters import TitleFilter
from .mixins import CustomMixinViewSet
from .permissions import (AdminAuthorModeratorOrReadOnly, IsAdmin,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadOnlySerializer, TitleSerializer,
                          TokenSerializer, UserMeSerializer,
                          UserRegistrationSerializer, UserSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, )
    filter_backends = (SearchFilter, )
    filterset_fields = ('username',)
    search_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options', 'trace']

    @action(
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserMeSerializer,
        detail=False,
        url_path='me',
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUser(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = str(uuid.uuid4())
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject="YaMDb registration",
            message=f"Your confirmation code: {confirmation_code}",
            from_email=ADMIN_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )
        return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if code == user.confirmation_code:
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(CustomMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CustomMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('genre',)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadOnlySerializer

        return super().get_serializer_class()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminAuthorModeratorOrReadOnly
                          & IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AdminAuthorModeratorOrReadOnly
                          & IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
