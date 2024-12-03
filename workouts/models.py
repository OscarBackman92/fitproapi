# workouts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Workout(models.Model):
    """Model to represent a workout."""

    CARDIO = 'cardio'
    STRENGTH = 'strength'
    FLEXIBILITY = 'flexibility'
    SPORTS = 'sports'
    OTHER = 'other'

    WORKOUT_TYPES = [
        (CARDIO, 'Cardio'),
        (STRENGTH, 'Strength Training'),
        (FLEXIBILITY, 'Flexibility'),
        (SPORTS, 'Sports'),
        (OTHER, 'Other'),
    ]

    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'

    INTENSITY_LEVELS = [
        (LOW, 'Low'),
        (MODERATE, 'Moderate'),
        (HIGH, 'High'),
    ]

    title = models.CharField(
        max_length=200,
        default="My Workout",
        help_text="Title of the workout"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts',
        db_index=True
    )
    workout_type = models.CharField(
        max_length=100,
        choices=WORKOUT_TYPES,
        db_index=True
    )
    date_logged = models.DateField(
        default=timezone.now,
        db_index=True
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        help_text="Duration in minutes"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the workout"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intensity = models.CharField(
        max_length=20,
        choices=INTENSITY_LEVELS,
        default=MODERATE,
        db_index=True
    )

    def __str__(self):
        return f'{self.title} - {self.get_workout_type_display()}'

    class Meta:
        ordering = ['-date_logged']
