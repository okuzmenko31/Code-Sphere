from notifications.models import Notification
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from .serializers import NotificationSerializer


class NotificationsAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)


class UnreadNotificationsAPIView(NotificationsAPIView):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(unread=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.queryset.update(unread=False)
        return response
