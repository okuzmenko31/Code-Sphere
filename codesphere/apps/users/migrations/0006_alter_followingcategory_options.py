# Generated by Django 4.2.1 on 2023-05-25 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_followingcategory_alter_userprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followingcategory',
            options={'verbose_name': 'following category', 'verbose_name_plural': 'Following categories'},
        ),
    ]
