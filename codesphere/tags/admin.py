from django.contrib import admin
from .models import Tags, TagSubscribers


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['name']


@admin.register(TagSubscribers)
class TagSubscribersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tag']
    list_display_links = ['id']
    search_fields = ['id', 'user', 'tag']
