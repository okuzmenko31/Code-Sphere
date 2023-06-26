from django.urls import path
from .views import CommentsListCreateAPIView, CommentDetailAPIView

urlpatterns = [
    path('<int:comment_id>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path(f'<str:instance_value>/<int:instance_id>/',
         CommentsListCreateAPIView.as_view(),
         name='comments_list_create')
]
