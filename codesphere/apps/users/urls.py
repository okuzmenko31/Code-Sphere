from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserRegistrationAPIView,
                    ConfirmEmailAPIView,
                    LoginAPIView,
                    LogoutAPIView,
                    ChangeEmailAPIView,
                    ChangeEmailConfirmAPIView,
                    SendPasswordResetAPIView,
                    PasswordResetAPIView,
                    UserProfileViewSet,
                    NotificationsAPIView,
                    UnreadNotificationsAPIView)

router = DefaultRouter()
router.register(r'profile', viewset=UserProfileViewSet, basename='profile')

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('confirm_email/<token>/<email>/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change_email/', ChangeEmailAPIView.as_view(), name='change_email_send'),
    path('change_email_confirm/<token>/<email>/',
         ChangeEmailConfirmAPIView.as_view(),
         name='change_email_confirm'),
    path('password_reset/', SendPasswordResetAPIView.as_view(), name='send_password_reset'),
    path('password_reset/<token>/<email>/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('', include(router.urls)),
    path('notifications/all/', NotificationsAPIView.as_view(), name='user_notifications'),
    path('notifications/unread/', UnreadNotificationsAPIView.as_view(), name='user_unread_notifications'),
]
