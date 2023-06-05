from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not UserProfile.objects.filter(user_id=instance.id).exists():
        UserProfile.objects.create(user=instance)
