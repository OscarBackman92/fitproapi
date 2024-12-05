from django.db import models
from django.contrib.auth.models import User
from workouts.models import Workout

class WorkoutPost(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workout_posts'
    )
    workout = models.OneToOneField(
        Workout,
        on_delete=models.CASCADE,
        related_name='post'
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s post: {self.workout.title}"
