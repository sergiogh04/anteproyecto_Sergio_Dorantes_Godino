from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Anime, Genre

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'status', 'year', 'is_trending', 'is_seasonal')
    list_filter = ('format', 'status', 'year', 'is_trending', 'is_seasonal')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_trending', 'is_seasonal')

admin.site.register(Genre)
