from django.db import models
from django.contrib.auth.models import User
from workoutposts.models import WorkoutPost


class Like(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        WorkoutPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'post']

    def __str__(self):
        return f"{self.owner} likes {self.post}"
