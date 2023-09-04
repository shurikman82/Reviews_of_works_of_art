from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import generics, viewsets, permissions
from rest_framework import filters, pagination, viewsets
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TokenSerializer,
                          ReviewSerializer, UserSerializer,
                          UserMeSerializer, UserRegistrationSerializer)
from reviews.models import Category, Genre, Title, Review
from .permissions import AdminAuthorModeratorOrReadOnly, IsAdmin


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, )
    filter_backends = (DjangoFilterBackend, )
    search_fields = ('username', )

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(
        methods=['get', 'patch', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateUser(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            username=request.data['username'],
            email=request.data['email'],
        )
        confirmation_code = user.make_confirmation_code()
        send_mail(
            subject="YaMDb registration",
            message=f"Your confirmation code: {confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (AdminAuthorModeratorOrReadOnly,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
