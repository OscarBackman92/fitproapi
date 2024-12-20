# Generated by Django 5.1.2 on 2024-12-05 09:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
        ('workoutposts', '0002_alter_workoutpost_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('owner', 'post')},
        ),
    ]
