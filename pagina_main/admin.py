from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfiles'
    fields = ('profile_picture', 'bio', 'birth_date')
    readonly_fields = ('profile_picture_preview',)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(
                f'<img src="{obj.profile_picture.url}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />')
        return "No hay imagen"

    profile_picture_preview.short_description = 'Vista Previa'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'profile_picture_tag')
    search_fields = ('user__username', 'bio')

    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return mark_safe(
                f'<img src="{obj.profile_picture.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />')
        return "No hay imagen"

    profile_picture_tag.short_description = 'Imagen'