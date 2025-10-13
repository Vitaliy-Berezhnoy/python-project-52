from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "username"]
    list_display = ["username", "first_name", "last_name", "created_at"]
    list_filter = (("created_at", DateFieldListFilter),)
