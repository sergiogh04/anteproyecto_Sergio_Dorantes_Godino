from django.contrib import admin

# Register your models here.

from animes.models import Studio, Anime, Genre


admin.site.register(Studio)
admin.site.register(Anime)
admin.site.register(Genre)

