from django.contrib import admin
from .models import FollowingCategory, Following


@admin.register(FollowingCategory)
class FollowingCategoryAdmin(admin.ModelAdmin):
    exclude = ['object_id', 'content_object']


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    pass
