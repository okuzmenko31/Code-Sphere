# Generated by Django 4.2.1 on 2023-06-21 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_posts_created_posts_updated'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostLikes',
        ),
    ]
