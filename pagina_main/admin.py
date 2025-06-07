from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import (
    Anime,Genre,UserAnime,Profile
)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'status', 'year', 'is_trending', 'is_seasonal')
    list_filter = ('format', 'status', 'year', 'is_trending', 'is_seasonal')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_trending', 'is_seasonal')

@admin.register(UserAnime)
class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'status', 'score', 'added_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'anime__title')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

admin.site.register(Genre)
