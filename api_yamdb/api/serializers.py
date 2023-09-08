from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CustomValidateSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value == r'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено!'
            )
        return value

    def validate(self, data):
        if User.objects.filter(email=data.get('email'),
                               username=data.get('username')).exists():
            return data
        elif User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Такой email уже используется!'
            )
        elif User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Такое имя пользователя уже используется!'
            )
        return data


class UserSerializer(CustomValidateSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150, required=True, validators=(
            RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        lookup_field = 'username'
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


class UserRegistrationSerializer(CustomValidateSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150, required=True, validators=(
            RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )

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
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


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
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'genre', 'category',
                  'rating', 'year', 'description')
        read_only_fields = ('id', 'name', 'genre', 'category',
                            'rating', 'year', 'description')


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
