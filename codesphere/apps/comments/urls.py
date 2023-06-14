from django.urls import path
from .views import CommentsListAPIView, CommentsCreateAPIView

urlpatterns = [
    path('', CommentsListAPIView.as_view(), name='comments'),
    path(f'add_comment/<str:instance_value>/<int:instance_id>/',
         CommentsCreateAPIView.as_view(),
         name='add_comment')
]
