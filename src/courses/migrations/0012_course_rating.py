# Generated by Django 5.1.4 on 2024-12-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_course_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
