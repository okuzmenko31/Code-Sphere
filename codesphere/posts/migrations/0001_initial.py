# Generated by Django 4.1.7 on 2023-03-27 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simplemde.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0004_alter_tagsubscribers_tag_alter_tagsubscribers_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title of post')),
                ('text', simplemde.fields.SimpleMDEField(verbose_name='Text')),
                ('cover_photo', models.ImageField(upload_to='images/posts/', verbose_name='Cover of post')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Post confirmed')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Creator of post')),
                ('likes', models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('tags', models.ManyToManyField(related_name='posts', to='tags.tags', verbose_name='Post tags')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['title'],
            },
        ),
    ]
