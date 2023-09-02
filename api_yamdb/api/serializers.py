from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'description',
                  'year', 'genre', 'rating', 'category')

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]
