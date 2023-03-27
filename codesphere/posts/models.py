from django.contrib.auth import get_user_model
from django.db import models
from tags.models import Tags
from mdeditor.fields import MDTextField

User = get_user_model()


class Posts(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='Creator of post',
                                related_name='posts')

    title = models.CharField(max_length=500,
                             verbose_name='Title of post')
    text = MDTextField(verbose_name='Text')
    cover_photo = models.ImageField(upload_to='images/posts/',
                                    verbose_name='Cover of post')
    tags = models.ManyToManyField(Tags,
                                  verbose_name='Post tags',
                                  related_name='posts')
    likes = models.ManyToManyField(User,
                                   verbose_name='Likes',
                                   related_name='liked_posts')
    is_confirmed = models.BooleanField(default=False,
                                       verbose_name='Post confirmed')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['title']

    def __str__(self):
        return f'Post # {self.id}, creator: {self.creator}'
