from django.urls import path
from .views import CommentsCreateAPIView, CommentDetailAPIView

urlpatterns = [
    path('<int:comment_id>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path(f'<str:instance_value>/<int:instance_id>/',
         CommentsCreateAPIView.as_view(),
         name='add_comment')
]
