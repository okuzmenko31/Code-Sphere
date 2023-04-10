# Generated by Django 4.2 on 2023-04-10 15:11

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0004_alter_tagsubscribers_tag_alter_tagsubscribers_user'),
        ('users', '0012_token_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewersIPs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100, verbose_name='Viewer IP')),
            ],
            options={
                'verbose_name': 'viewer',
                'verbose_name_plural': 'Post viewers',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title of post')),
                ('short_description', models.TextField(max_length=2000, verbose_name='Short description of post')),
                ('text', mdeditor.fields.MDTextField(verbose_name='Text')),
                ('cover_photo', models.ImageField(upload_to='images/posts/', verbose_name='Cover of post')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Post confirmed')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.userprofile', verbose_name='Creator of post')),
                ('tags', models.ManyToManyField(related_name='posts', to='tags.tags', verbose_name='Post tags')),
                ('views', models.ManyToManyField(blank=True, related_name='posts', to='posts.viewersips')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PostLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='posts.posts', verbose_name='Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='users.userprofile', verbose_name='User')),
            ],
            options={
                'verbose_name': 'like',
                'verbose_name_plural': 'Likes',
            },
        ),
    ]
