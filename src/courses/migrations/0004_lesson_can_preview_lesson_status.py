# Generated by Django 5.1.4 on 2024-12-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='can_preview',
            field=models.BooleanField(default=False, help_text='Can user without course access see this?'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('pub', 'Published'), ('soon', 'Coming Soon'), ('draft', 'Draft')], default='pub', max_length=15),
        ),
    ]
