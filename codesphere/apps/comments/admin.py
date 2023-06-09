from django.contrib import admin
from .models import Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'instance_type']
    list_display_links = ['id', 'instance_type']
