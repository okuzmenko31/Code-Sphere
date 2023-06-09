# Generated by Django 4.2.1 on 2023-05-24 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email')),
                ('username', models.CharField(blank=True, max_length=250, unique=True, verbose_name='Username')),
                ('full_name', models.CharField(blank=True, max_length=250, verbose_name='Full name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser status')),
                ('is_active', models.BooleanField(default=True, verbose_name='User activated')),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
