from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User
from apps.content_type_instances.utils import MODEL_INSTANCES_TYPES


class Comments(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='comments')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               verbose_name='Parent',
                               blank=True,
                               null=True)
    text = models.TextField(max_length=10000,
                            verbose_name='Comment text')
    instance_type = models.CharField(max_length=32,
                                     verbose_name='Instance type',
                                     choices=MODEL_INSTANCES_TYPES,
                                     blank=True)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id'])
        ]

    def __str__(self):
        return f'Comment to: {self.content_object}'
