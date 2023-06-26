from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from apps.users.models import User
from apps.content_type_instances.utils import MODEL_INSTANCES_TYPES


class Likes(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='user_likes')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    instance_type = models.CharField(max_length=32,
                                     verbose_name='Instance type',
                                     choices=MODEL_INSTANCES_TYPES,
                                     blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'Likes'
        indexes = [
            models.Index(fields=['content_type', 'object_id'])
        ]

    def __str__(self):
        return f'Like from {self.creator.username}'
