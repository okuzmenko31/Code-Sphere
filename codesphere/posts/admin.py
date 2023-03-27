from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'is_confirmed']
    list_display_links = ['id']
    search_fields = ['id', 'creator']
    list_editable = ['creator', 'is_confirmed']
    list_filter = ['is_confirmed']
    exclude = ['likes']
