# Generated by Django 4.2 on 2023-04-10 17:02

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('comments', '0002_alter_comment_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=10000, verbose_name='Comment'),
        ),
    ]
