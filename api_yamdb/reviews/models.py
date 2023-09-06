from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        choices=ROLE_CHOICES,
        verbose_name='Роль пользователя',
        max_length=9, default='user',
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, max_length=128)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        verbose_name='Идентификатор категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='Идентификатор жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    genre = models.ManyToManyField(
        Genre, through='TitleGenre',
        verbose_name='Жанр произведения',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, verbose_name='Категория произведения',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='title_genre',
    )

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        verbose_name='Жанр произведения',
        related_name='title_genre',
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self) -> str:
        return f'Жанр произведения {self.name} - {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.CharField(verbose_name='Текст отзыва', max_length=255)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка произведения в баллах от 1 до 10.'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение, к которому относится отзыв.'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор комментария'
    )
    text = models.CharField(verbose_name='Текст комментария', max_length=255)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв, к которому относится комментарий.',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
