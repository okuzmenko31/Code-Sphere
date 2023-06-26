from django.contrib import admin
from .models import Likes


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'instance_type']
    list_display_links = ['id', 'instance_type']
