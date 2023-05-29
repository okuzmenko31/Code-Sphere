from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'title', 'is_confirmed']
    list_display_links = ['id', 'title']
    list_editable = ['is_confirmed']
    search_fields = ['id', 'creator', 'title', 'is_confirmed']
