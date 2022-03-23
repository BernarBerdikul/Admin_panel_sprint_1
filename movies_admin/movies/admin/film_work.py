from datetime import datetime, timedelta

import requests
from django import forms
from django.conf import settings
from django.contrib import admin

from ..models import FilmWork, GenreFilmWork, PersonFilmWork
from ..state import state


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
    title = "Показать фильмы с рейтингом в промежутке:"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "rating"

    def lookups(self, request, model_admin) -> tuple:
        """Return Enum for filter"""
        return (
            ("1-2", "от 1 до 2"),
            ("2-3", "от 2 до 3"),
            ("3-4", "от 3 до 4"),
            ("4-5", "от 4 до 5"),
            ("5-6", "от 5 до 6"),
            ("6-7", "от 6 до 7"),
            ("7-8", "от 7 до 8"),
            ("8-9", "от 8 до 9"),
            ("9-10", "от 9 до 10"),
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the value"""
        if self.value():
            _range: list = self.value().split("-")  # Example: ['8', '9']
        else:
            _range: list = [1, 10]
        return queryset.filter(rating__range=_range)


def get_remote_roles() -> list[tuple]:
    try:
        roles_data = requests.get(url=settings.AUTH_SERVICE_URL).json()
        roles_choices: list[tuple] = [
            (role.get("name"), role.get("name"))
            for role in roles_data.get("data")[0].get("roles")
        ]
        roles_choices.insert(0, ("anonymous", "anonymous"))
        state.set_state(key="roles", value=f"{roles_choices}")
        expire_time = datetime.now() + timedelta(minutes=5)
        state.set_state(key="expire_time", value=int(expire_time.timestamp()))
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        roles_choices: list[tuple] = eval(state.get_state(key="roles"))
    return roles_choices


class FilmWorkForm(forms.ModelForm):
    if int(state.get_state(key="expire_time")) < datetime.now().timestamp():
        roles_choices: list[tuple] = get_remote_roles()
    else:
        roles_choices: list[tuple] = eval(state.get_state(key="roles"))
    roles = forms.MultipleChoiceField(choices=roles_choices)


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
        "roles",
    )
    list_filter = (RatingListFilter,)
    form = FilmWorkForm
    search_fields = ("title",)

    inlines = [PersonInline, GenreInline]
