from django.contrib import admin
from ..models import FilmWork, PersonFilmWork, GenreFilmWork


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


class RatingListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Показать фильмы с рейтингом в промежутке:'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        """Return Enum for filter"""
        return (
            ('1-2', 'от 1 до 2'),
            ('2-3', 'от 2 до 3'),
            ('3-4', 'от 3 до 4'),
            ('4-5', 'от 4 до 5'),
            ('5-6', 'от 5 до 6'),
            ('6-7', 'от 6 до 7'),
            ('7-8', 'от 7 до 8'),
            ('8-9', 'от 8 до 9'),
            ('9-10', 'от 9 до 10'),
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the value"""
        if self.value():
            _range: list = self.value().split('-')  # Example: ['8', '9']
        else:
            _range: list = [1, 10]
        return queryset.filter(rating__range=_range)


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
    list_filter = (RatingListFilter,)
    search_fields = ("title",)

    inlines = [PersonInline, GenreInline]
