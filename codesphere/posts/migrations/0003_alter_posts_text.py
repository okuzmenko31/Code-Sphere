# Generated by Django 4.2 on 2023-05-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_posts_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
    ]
