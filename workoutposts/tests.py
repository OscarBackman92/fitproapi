from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from workouts.models import Workout

class WorkoutPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(
            user=self.user,
            title="Morning Run",
            workout_type="cardio",
            duration=30,
            intensity="moderate"
        )

    def test_create_post(self):
        response = self.client.post('/api/posts/posts/', {
            'user': self.user.id,
            'workout': self.workout.id,
            'content': 'Great workout!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        response = self.client.get('/api/posts/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)