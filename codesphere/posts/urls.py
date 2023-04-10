from django.urls import path
from .views import *

urlpatterns = [
    path('', AllPostsListView.as_view(), name='all-posts'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('like/<int:post_id>/', LikePost.as_view(), name='like_post'),
    path('post_comment/<int:post_id>/', AddPostComment.as_view(), name='add_comment')
]
