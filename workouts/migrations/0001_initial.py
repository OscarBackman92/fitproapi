# Generated by Django 5.1.2 on 2024-12-03 23:53

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='My Workout', help_text='Title of the workout', max_length=200)),
                ('workout_type', models.CharField(choices=[('cardio', 'Cardio'), ('strength', 'Strength Training'), ('flexibility', 'Flexibility'), ('sports', 'Sports'), ('other', 'Other')], db_index=True, max_length=100)),
                ('date_logged', models.DateField(db_index=True, default=django.utils.timezone.now)),
                ('duration', models.IntegerField(help_text='Duration in minutes', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1440)])),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the workout')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('intensity', models.CharField(choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')], db_index=True, default='moderate', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_logged'],
            },
        ),
    ]
