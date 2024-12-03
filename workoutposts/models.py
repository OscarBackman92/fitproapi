from django.db import models
from django.contrib.auth.models import User
from workouts.models import Workout

class WorkoutPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_posts")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.workout.workout_type} workout post"
