from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Users


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'user_name']
    list_display = ['user_name', 'first_name', 'last_name', 'created_at']
    list_filter = (('created_at', DateFieldListFilter),)

