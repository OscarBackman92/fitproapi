from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Workout


class WorkoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpass123')
        self.client.force_authenticate(user=self.user)

        self.workout_data = {
            'title': 'Morning Run',
            'workout_type': 'cardio',
            'duration': 30,
            'intensity': 'moderate',
            'notes': '5k run',
            'date_logged': '2024-03-14'
        }

        self.workout = Workout.objects.create(
            owner=self.user, **self.workout_data)

    def test_create_workout(self):
        response = self.client.post('/api/workouts/', self.workout_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertTrue(response.data['is_owner'])

    def test_list_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_workout(self):
        response = self.client.patch(
            f'/api/workouts/{self.workout.id}/',
            {'title': 'Updated Run'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Run')

    def test_delete_workout(self):
        response = self.client.delete(f'/api/workouts/{self.workout.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
