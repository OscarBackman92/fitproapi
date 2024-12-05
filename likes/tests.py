from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from workoutposts.models import WorkoutPost
from workouts.models import Workout
from .models import Like

class LikeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.workout = Workout.objects.create(
            owner=self.user, 
            title='Test Workout',
            workout_type='cardio',
            duration=30,
            intensity='moderate'
        )
        
        self.post = WorkoutPost.objects.create(
            owner=self.user,
            workout=self.workout,
            content='Test post'
        )

    def test_create_like(self):
        response = self.client.post('/api/likes/likes/', {
            'post': self.post.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_like(self):
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.post('/api/likes/likes/', {
            'post': self.post.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)