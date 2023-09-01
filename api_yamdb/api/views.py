from django.shortcuts import render
from .serializers import ReviewSerializer
# Create your views here.
from django.shortcuts import get_object_or_404
from reviews.models import Review
from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminAuthorModeratorOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
 






class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [AdminAuthorModeratorOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_title(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, pk=title_id)
    #     return title
    
    # def get(self, request):
    #     # Ваш код обработки запроса
    #     return Response({"message": "Доступ разрешен."})

    # def create(self, request, *args, **kwargs):
    #     required_fields = ['field1', 'field2', 'field3', ]  # Укажите обязательные поля здесь

    #     for field in required_fields:
    #         if field not in request.data:
    #             return Response({"error": f"Отсутствует обязательное поле: {field}"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Здесь вы можете продолжить обработку создания объекта, так как все обязательные поля присутствуют

    #     # Пример сохранения объекта
    #     # serializer = YourModelSerializer(data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message": "Объект успешно создан"}, status=status.HTTP_201_CREATED)
