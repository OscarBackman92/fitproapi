from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Comment
from workoutposts.models import WorkoutPost
from workouts.models import Workout

class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(
            user=self.user,
            title="Test Workout",
            workout_type="cardio",
            duration=30,
            intensity="moderate"
        )
        self.post = WorkoutPost.objects.create(
            user=self.user,
            workout=self.workout,
            content='Test post'
        )

    def test_create_comment(self):
        response = self.client.post('/api/comments/comments/', {
            'user': self.user.id,
            'post': self.post.id,
            'content': 'Great post!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comments(self):
        response = self.client.get('/api/comments/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)