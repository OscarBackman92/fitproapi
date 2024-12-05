# Generated by Django 5.1.2 on 2024-12-05 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutposts', '0001_initial'),
        ('workouts', '0002_rename_user_workout_owner_workout_is_published_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workoutpost',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='workoutpost',
            old_name='user',
            new_name='owner',
        ),
        migrations.AddField(
            model_name='workoutpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='workoutpost',
            name='workout',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='workouts.workout'),
        ),
    ]