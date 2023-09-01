from rest_framework import serializers

from reviews.models import Category, Genre, Title, TitleGenre, Review
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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'description',
                  'year', 'genre', 'rating', 'category')
        
    # def get_raiting(self, obj):
    #     ratings = obj.score.all()
    #     if not raitings:
    #         return 0
    #     total_rating = sum(ratings)
    #     average_rating = total_rating / len(ratings)
    #     return average_rating

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(Avg('score'))['score__avg']
        return rating
    
    def get_rating(self, obj):
        return 0

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title

        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title
    

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




