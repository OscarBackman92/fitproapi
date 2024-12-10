# Generated by Django 5.1.2 on 2024-12-09 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_profile_content_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]