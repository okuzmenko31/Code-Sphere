from django.db import models
from django.urls import reverse
from tags.models import Tags
from mdeditor.fields import MDTextField
from users.models import UserProfile, User


class ViewersIPs(models.Model):
    ip = models.CharField(max_length=100,
                          verbose_name='Viewer IP')

    class Meta:
        verbose_name = 'viewer'
        verbose_name_plural = 'Post viewers'

    def __str__(self):
        return f'Viewer IP: {self.ip}'


class PostLikes(models.Model):
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='likes')
    post = models.ForeignKey('Posts',
                             on_delete=models.CASCADE,
                             verbose_name='Post',
                             related_name='post_likes')

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'User: {self.user}, Post: {self.post}'


class Posts(models.Model):
    creator = models.ForeignKey(UserProfile,
                                on_delete=models.CASCADE,
                                verbose_name='Creator of post',
                                related_name='posts')

    title = models.CharField(max_length=500,
                             verbose_name='Title of post')
    short_description = models.TextField(max_length=2000,
                                         verbose_name='Short description of post')
    text = MDTextField(verbose_name='Text')
    cover_photo = models.ImageField(upload_to='images/posts/',
                                    verbose_name='Cover of post')
    tags = models.ManyToManyField(Tags,
                                  verbose_name='Post tags',
                                  related_name='posts')
    views = models.ManyToManyField(ViewersIPs,
                                   blank=True,
                                   related_name='posts')
    is_confirmed = models.BooleanField(default=False,
                                       verbose_name='Post confirmed')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['title']

    def __str__(self):
        return f'Post # {self.id}, creator: {self.creator}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.id})

    def post_views(self):
        return self.views.count()
