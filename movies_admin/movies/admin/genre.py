from django.contrib import admin
from ..models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    fields = ("name", "description")
    search_fields = ("name",)
