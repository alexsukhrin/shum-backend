# Generated by Django 5.1.11 on 2025-07-23 13:10

import shum.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='User profile picture (stored in S3)', null=True, upload_to=shum.users.models.user_avatar_path, verbose_name='Avatar'),
        ),
    ]
