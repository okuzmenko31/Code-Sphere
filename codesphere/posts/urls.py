from django.urls import path
from .views import *

urlpatterns = [
    path('', AllPostsListView.as_view(), name='all-posts'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:post_id>/', PostDetail.as_view(), name='post_detail')
]
