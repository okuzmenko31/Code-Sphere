from django.urls import path
from .views import (PostsAPIView,
                    PostDetailAPIView,
                    UnconfirmedPostsAPIView,
                    UnconfirmedPostsDetailAPIView,
                    LikedPostsListAPIView,
                    BestPostsListAPIView)

urlpatterns = [
    path('', PostsAPIView.as_view(), name='posts'),
    path('<int:post_id>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('unconfirmed/', UnconfirmedPostsAPIView.as_view(), name='unconfirmed_posts'),
    path('unconfirmed/<int:post_id>/',
         UnconfirmedPostsDetailAPIView.as_view(),
         name='unconfirmed_posts_detail'),
    path('liked/',
         LikedPostsListAPIView.as_view(),
         name='liked_posts'),
    path('best/',
         BestPostsListAPIView.as_view(),
         name='best_posts')
]
