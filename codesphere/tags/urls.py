from django.urls import path
from .views import *

urlpatterns = [
    path('', AllTagsListView.as_view(), name='all-tags'),
    path('subscribe/<int:tag_id>/', SubscribeTag.as_view(), name='tag-subscribe')
]
