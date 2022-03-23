from django.contrib import admin

from ..models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["full_name"]
    list_display_links = ["full_name"]
    fields = ("full_name", "birth_date")
    search_fields = ("full_name",)
