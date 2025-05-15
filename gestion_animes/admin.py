from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Anime, Review, UserAnimeList

class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'rating', 'start_date')
    search_fields = ('title', 'categories')
    list_filter = ('status', 'categories')
    ordering = ('-created_at',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'rating', 'created_at')
    search_fields = ('user__username', 'anime__title')
    list_filter = ('rating',)

admin.site.register(Anime, AnimeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserAnimeList)