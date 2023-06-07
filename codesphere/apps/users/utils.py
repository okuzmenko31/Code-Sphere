from notifications.models import Notification

from .models import User, UserProfile


def create_user_profile(user: User):
    if user.is_active and not UserProfile.objects.filter(user_id=user.id).exists():
        UserProfile.objects.create(user=user)
