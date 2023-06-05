from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from apps.users.models import User


class FollowingCategory(models.Model):
    name = models.CharField(max_length=32,
                            verbose_name='Following category')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     verbose_name='Following object model')
    object_id = models.PositiveIntegerField(blank=True,
                                            null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = 'following category'
        verbose_name_plural = 'Following categories'

    def __str__(self):
        return f'Following category: {self.name}'


class Following(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='followings')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    following_category = GenericRelation(FollowingCategory,
                                         on_delete=models.CASCADE)

    # about GenericRelation:
    # https://docs.djangoproject.com/en/4.2/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericRelation

    class Meta:
        verbose_name = 'following'
        verbose_name_plural = 'Followings'

    def __str__(self):
        return f'Follower: {self.user.username}'
