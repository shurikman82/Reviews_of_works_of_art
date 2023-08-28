from django.db import models


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
    year = models.IntegerField(max_length=4, verbose_name='Год выпуска')
    genre = models.ManyToManyField(
        Genre, on_delete=models.SET_NULL,
        null=True, through='TitleGenre',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр произведения')

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self) -> str:
        return f'Жанр произведения {self.name} - {self.genre}'
