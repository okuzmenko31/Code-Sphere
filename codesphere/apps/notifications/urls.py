from django.urls import path
from .views import NotificationsAPIView, UnreadNotificationsAPIView

urlpatterns = [
    path('all/', NotificationsAPIView.as_view(), name='all_notifications'),
    path('unread/', UnreadNotificationsAPIView.as_view(), name='unread_notifications'),
]
