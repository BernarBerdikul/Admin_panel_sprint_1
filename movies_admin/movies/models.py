from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .mixins import UUIDMixin, CreateTimeMixin, UpdateTimeMixin


class FilmWorkType(models.TextChoices):
    MOVIE = "movie", _("Фильм")
    TV_SHOW = "tv_show", _("Теле шоу")


class PersonType(models.TextChoices):
    ACTOR = "actor", _("Актер")
    DIRECTOR = "director", _("Режиссер")
    WRITER = "writer", _("Сценарист")


class Genre(UUIDMixin, UpdateTimeMixin):
    name = models.CharField(max_length=30, verbose_name=_("Название"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        db_table = 'content"."genre'

    def __str__(self):
        return self.name


class Person(UUIDMixin, UpdateTimeMixin):
    full_name = models.CharField(max_length=60, verbose_name=_("Имя фамилия"))
    birth_date = models.DateField(
        blank=True, null=True, verbose_name=_("Дата рождения")
    )

    class Meta:
        verbose_name = _("Персона")
        verbose_name_plural = _("Персоны")
        db_table = 'content"."person'

    def __str__(self):
        return self.full_name


class GenreFilmWork(UUIDMixin, CreateTimeMixin):
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)

    class Meta:
        db_table = 'content"."genre_film_work'
        unique_together = (("film_work", "genre"),)

    def __str__(self):
        return f"{self.film_work.title} - {self.genre.name}"


class PersonFilmWork(UUIDMixin, CreateTimeMixin):
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.CharField(
        max_length=30,
        choices=PersonType.choices,
        default=PersonType.ACTOR,
        verbose_name=_("Роль в фильме")
    )

    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = (("film_work", "person", "role"),)

    def __str__(self):
        return f"{self.film_work.title} - {self.person.full_name} - {self.role}"


class FilmWork(UUIDMixin, UpdateTimeMixin):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    creation_date = models.DateField(
        blank=True, null=True, verbose_name=_("Дата создания")
    )
    certificate = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Сертификат")
    )
    file_path = models.FileField(
        upload_to=f"{settings.MEDIA_ROOT}/film_works/",
        blank=True,
        verbose_name=_("Файл"),
    )
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True, verbose_name=_("Рейтинг")
    )
    type = models.CharField(
        max_length=30,
        choices=FilmWorkType.choices,
        verbose_name=_("Тип кинопроизведения"),
    )
    genres = models.ManyToManyField(
        Genre, through="GenreFilmWork", verbose_name=_("Жанр")
    )
    persons = models.ManyToManyField(
        Person, through="PersonFilmWork", verbose_name=_("Актеры")
    )

    class Meta:
        verbose_name = _("Кинопроизведение")
        verbose_name_plural = _("Кинопроизведения")
        db_table = 'content"."film_work'

    def __str__(self):
        return f"{self.title} - {self.type} - {self.rating}"
