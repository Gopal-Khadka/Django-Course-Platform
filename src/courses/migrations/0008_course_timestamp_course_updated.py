# Generated by Django 5.1.4 on 2024-12-17 14:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_lesson_options_lesson_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
