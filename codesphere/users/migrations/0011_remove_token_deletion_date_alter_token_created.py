# Generated by Django 4.1.7 on 2023-04-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_token_deletion_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='deletion_date',
        ),
        migrations.AlterField(
            model_name='token',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Token creation date'),
        ),
    ]
