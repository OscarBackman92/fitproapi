from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from workouts.models import Workout
from .models import WorkoutPost

class WorkoutPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.workout = Workout.objects.create(
            owner=self.user,  # Changed from user to owner
            title='Test Workout',
            workout_type='cardio',
            duration=30,
            intensity='moderate',
            date_logged='2024-03-14'
        )

    def test_create_post(self):
        response = self.client.post('/api/posts/posts/', {
            'workout': self.workout.id,
            'content': 'Test post content'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        response = self.client.get('/api/posts/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('likes_count', response.data['results'][0])
        self.assertIn('comments_count', response.data['results'][0])