from django.db.models import Avg
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150, required=True, validators=(
            RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Invalid value of username')
        return value

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )
        lookup_field = 'username'
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150, required=True, validators=(
            RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    def validate(self, data):
        if User.objects.filter(email=data.get('email'),
                               username=data.get('username')):
            return data
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                {
                    "error": "Email is already used!"
                }
            )
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                {
                    "error": "Username is already used!"
                }
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        read_only_fields = ['role']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'description',
                  'year', 'genre', 'category')


class TitleReadOnlySerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'genre', 'category',
                  'rating', 'year', 'description')
        read_only_fields = ('id', 'name', 'genre', 'category',
                            'rating', 'year', 'description')

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        review = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')
        )
        if review and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы можете оставить только 1 отзыв к произведению!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'review')
