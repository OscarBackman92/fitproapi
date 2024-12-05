from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from workoutposts.models import WorkoutPost
from workouts.models import Workout
from .models import Comment

class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.workout = Workout.objects.create(
            owner=self.user,
            title='Test Workout',
            workout_type='cardio',
            duration=30
        )
        
        self.post = WorkoutPost.objects.create(
            owner=self.user,
            workout=self.workout,
            content='Test post'
        )

    def test_create_comment(self):
        response = self.client.post('/api/comments/comments/', {
            'post': self.post.id,
            'content': 'Test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comments(self):
        Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        response = self.client.get('/api/comments/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
