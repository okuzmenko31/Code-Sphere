from django.contrib import admin
from .models import User, UserProfile, Token
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = ((None, {'fields': ('email', 'username', 'password',
                                    'full_name', 'last_login',)},),
                 (
                     'Permissions', {
                         'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions',)},),)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'full_name', 'password1', 'password2'),
            },
        ),
    )

    list_display = ('email', 'full_name', 'username', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id']
    list_editable = ['user']
    search_fields = ['id', 'user', 'city', 'country']
    list_filter = ['city', 'country']


admin.site.register(Token)
