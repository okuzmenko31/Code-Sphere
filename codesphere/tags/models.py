from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Tags(models.Model):
    """Model of tags"""

    name = models.CharField(max_length=450,
                            unique=True,
                            verbose_name='Tag name')
    description = models.TextField(max_length=2000,
                                   verbose_name='Tag description')
    icon = models.ImageField(upload_to='images/tags/',
                             verbose_name='Tag icon',
                             blank=True)
    slug = models.SlugField(unique=True,
                            verbose_name='Tag slug',
                            blank=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return f'Tag: {self.name}'

    def save(self, *args, **kwargs):
        """Saving tag slug as slugify tag name"""
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)


class TagSubscribers(models.Model):
    """Model of tag subscribers"""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Subscriber')
    tag = models.ForeignKey(Tags,
                            on_delete=models.CASCADE,
                            verbose_name='Tag')

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return f'Subscriber: {self.user}, tag: {self.tag.name}'
