from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import UserProfile


class Comment(models.Model):
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE,
                             verbose_name='Writer')
    text = models.TextField(max_length=10000, verbose_name='Comment')
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Creation date')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     verbose_name='Related object',
                                     related_name='comments')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Writer: {self.user.user.username}'
