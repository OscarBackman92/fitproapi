from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Workout


class WorkoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        self.workout_data = {
            'title': 'Morning Run',
            'workout_type': 'cardio',
            'duration': 30,
            'intensity': 'moderate',
        }
        self.workout = self.client.post('/workouts/', self.workout_data).data

    def test_list_workouts(self):
        response = self.client.get('/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_retrieve_workout(self):
        response = self.client.get(f"/workouts/{self.workout['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Morning Run')

    def test_update_workout(self):
        response = self.client.patch(f"/workouts/{self.workout['id']}/", {'title': 'Evening Run'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Evening Run')

    def test_delete_workout(self):
        response = self.client.delete(f"/workouts/{self.workout['id']}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
