# Generated by Django 4.2.1 on 2023-06-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_posts_cover_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='notifications_sent',
            field=models.BooleanField(default=False, verbose_name='Notifications about post was sent'),
        ),
    ]
