# Generated by Django 4.2.1 on 2023-06-14 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comments_created_comments_parent_comments_updated_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user',
            new_name='creator',
        ),
    ]
