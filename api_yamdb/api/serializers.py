from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150, required=True, validators=(
            RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )
    role = serializers.CharField(max_length=254, required=False)

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
