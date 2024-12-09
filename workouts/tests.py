from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Workout
from django.utils import timezone

class WorkoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpass123")
        self.client.login(username="testuser", password="testpass123")
        
        self.workout_data = {
            "title": "Morning Run",
            "workout_type": "cardio",
            "duration": 30,
            "intensity": "moderate",
            "date_logged": timezone.now().date(),
        }
        self.workout = Workout.objects.create(owner=self.user, **self.workout_data)

    def test_list_workouts(self):
        response = self.client.get("/workouts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])

    def test_create_workout(self):
        response = self.client.post("/workouts/", self.workout_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Morning Run")

    def test_retrieve_workout(self):
        response = self.client.get(f"/workouts/{self.workout.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.workout_data["title"])

    def test_update_workout(self):
        response = self.client.patch(f"/workouts/{self.workout.id}/", {"title": "Evening Run"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Evening Run")

    def test_delete_workout(self):
        response = self.client.delete(f"/workouts/{self.workout.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_workout_statistics(self):
        response = self.client.get("/workouts/statistics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_workouts"], 1)
        self.assertEqual(response.data["total_duration"], 30)
