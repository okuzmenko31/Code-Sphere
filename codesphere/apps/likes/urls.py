from django.urls import path
from .views import LikesListCreateAPIView, LikeDetailAPIView

urlpatterns = [
    path(f'<str:instance_value>/<int:instance_id>/',
         LikesListCreateAPIView.as_view(),
         name='likes_list_create'),
    path('<int:like_id>/',
         LikeDetailAPIView.as_view(),
         name='like_detail')
]
