# Generated by Django 4.2.1 on 2023-05-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=170, verbose_name='Tag name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/tags', verbose_name='Tag image')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'Tags',
            },
        ),
    ]
