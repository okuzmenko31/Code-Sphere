from django.urls import path
from .views import FollowAPIView

urlpatterns = [
    path('follow/<int:category_id>/<int:following_id>/',
         FollowAPIView.as_view(),
         name='follow')
]
