from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.followings.utils import get_post_creator_followers
from apps.notifications.utils import NotificationsMixin
from apps.tags.models import Tags
from apps.users.models import User


class ViewersIPs(models.Model):
    ip = models.CharField(max_length=100,
                          verbose_name='Viewer IP')

    class Meta:
        verbose_name = 'viewer'
        verbose_name_plural = 'Post viewers'

    def __str__(self):
        return f'Viewer IP: {self.ip}'


class PostLikes(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='post_likes')
    post = models.ForeignKey('Posts',
                             on_delete=models.CASCADE,
                             verbose_name='Post',
                             related_name='post_likes')

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'User: {self.user}, Post: {self.post}'


def post_image_upload_path(instance, filename):
    return f'posts/{instance.id}/{filename}'


class Posts(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='Creator of post',
                                related_name='posts')
    title = models.CharField(max_length=500,
                             verbose_name='Title of post')
    short_description = models.TextField(max_length=2000,
                                         verbose_name='Short description of post')
    text = models.TextField(verbose_name='Text')
    cover_photo = models.ImageField(upload_to=post_image_upload_path,
                                    verbose_name='Cover of post')
    tags = models.ManyToManyField(Tags,
                                  verbose_name='Post tags',
                                  related_name='posts')
    views = models.ManyToManyField(ViewersIPs,
                                   blank=True,
                                   related_name='posts')
    is_confirmed = models.BooleanField(default=False,
                                       verbose_name='Post confirmed')
    notifications_sent = models.BooleanField(default=False,
                                             verbose_name='Notifications about post was sent')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['title']

    def __str__(self):
        return f'Post # {self.id}, creator: {self.creator}'

    @property
    def get_notification_message(self) -> str:
        post_url = reverse('post_detail', kwargs={'post_id': self.id})
        message = f'{self.creator.username} made a new post , check it by this link: {post_url}'
        return message

    @property
    def get_creator_followers(self):
        return get_post_creator_followers(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_confirmed and not self.notifications_sent:
            notification_mixin = NotificationsMixin()
            notification_mixin.use_description = True
            message = self.get_notification_message
            notification_mixin.notification_message = message
            notification_mixin.description_message = notification_mixin.addition_message
            creator_followers = self.get_creator_followers
            notification_mixin.send_mass_notifications(sender=self.creator,
                                                       recipients=creator_followers)
            self.notifications_sent = True

    @property
    def post_views(self):
        return self.views.count()
