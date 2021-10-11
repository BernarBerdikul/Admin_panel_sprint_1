from django.contrib import admin
from .models import Genre, FilmWork, Person, PersonFilmWork, GenreFilmWork


class PersonInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ("person",)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person", "film_work")


class GenreInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ("genre",)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("genre", "film_work")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ("name", "description")
    search_fields = ("name",)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "rating"]
    list_display_links = ["title"]
    fields = (
        "title",
        "description",
        "creation_date",
        "certificate",
        "file_path",
        "rating",
        "type",
    )
    search_fields = ("title",)

    inlines = [PersonInline, GenreInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["full_name"]
    list_display_links = ["full_name"]
    fields = ("full_name", "birth_date")
    search_fields = ("full_name",)
