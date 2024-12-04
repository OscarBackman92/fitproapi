from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Workout

class WorkoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
        # Clear any existing workouts
        Workout.objects.all().delete()
        self.workout_data = {
            'title': 'Morning Run',
            'workout_type': 'cardio',
            'duration': 30,
            'intensity': 'moderate',
            'notes': '5k run',
            'date_logged': '2024-03-14'
        }
        self.workout = Workout.objects.create(user=self.user, **self.workout_data)

    def test_list_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Morning Run')

    def test_create_workout(self):
        new_workout = {
            'title': 'Evening Weights',
            'workout_type': 'strength',
            'duration': 45,
            'intensity': 'high',
            'notes': 'Upper body',
            'date_logged': '2024-03-14'
        }
        response = self.client.post('/api/workouts/', new_workout)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)

    def test_get_workout_detail(self):
        response = self.client.get(f'/api/workouts/{self.workout.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Morning Run')

    def test_update_workout(self):
        update_data = {
            'title': 'Updated Run',
            'duration': 35
        }
        response = self.client.patch(f'/api/workouts/{self.workout.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout.refresh_from_db()
        self.assertEqual(self.workout.title, 'Updated Run')

    def tearDown(self):
        User.objects.all().delete()
        Workout.objects.all().delete()