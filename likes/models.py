from django.db import models
from django.contrib.auth.models import User
from workoutposts.models import WorkoutPost

class Like(models.Model):
    """Like model for workout posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(WorkoutPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user.username} likes {self.post}"