# Generated by Django 4.2 on 2023-04-10 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0012_token_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000, verbose_name='Comment')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Related object')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='Writer')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
