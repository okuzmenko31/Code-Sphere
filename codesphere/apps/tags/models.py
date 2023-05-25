from django.db import models
from django.utils.text import slugify


class Tags(models.Model):
    name = models.CharField(max_length=170,
                            verbose_name='Tag name')
    image = models.ImageField(upload_to='photos/tags',
                              blank=True,
                              null=True,
                              verbose_name='Tag image')
    slug = models.SlugField(unique=True,
                            blank=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'Tag: {self.name}'

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)
        if not self.slug:
            self.slug = self.name
        super().save(*args, **kwargs)
