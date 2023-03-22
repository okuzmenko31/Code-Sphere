# Generated by Django 4.1.7 on 2023-03-22 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='images/user', verbose_name='Avatar')),
                ('bio', models.TextField(blank=True, max_length=700, verbose_name='Bio')),
                ('country', models.CharField(blank=True, max_length=150, verbose_name='Country')),
                ('city', models.CharField(blank=True, max_length=170, verbose_name='City')),
                ('twitter', models.URLField(blank=True, max_length=450, verbose_name='Twitter link')),
                ('facebook', models.URLField(blank=True, max_length=450, verbose_name='Facebook link')),
                ('github', models.URLField(blank=True, max_length=450, verbose_name='GitHub link')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
