# Generated by Django 4.2.1 on 2023-05-27 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0008_remove_following_following_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
