# Generated by Django 4.1.7 on 2023-04-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_token_deletion_date_alter_token_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='expired',
            field=models.BooleanField(default=False, verbose_name='Token expired'),
        ),
    ]