# Generated by Django 4.2 on 2023-04-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_alter_posts_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='short_description',
            field=models.TextField(default=1, max_length=2000, verbose_name='Short description of post'),
            preserve_default=False,
        ),
    ]
