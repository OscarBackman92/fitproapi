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

    def test_list_workouts_empty(self):
        """Test list endpoint when there are no workouts"""
        Workout.objects.all().delete()
        response = self.client.get("/workouts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_workouts(self):
        """Test listing workouts"""
        response = self.client.get("/workouts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])

    def test_create_workout_missing_fields(self):
        """Test creating a workout with missing required fields"""
        incomplete_data = {"workout_type": "cardio", "duration": 30}
        response = self.client.post("/workouts/", incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_workout_invalid_duration(self):
        """Test creating a workout with an invalid duration"""
        invalid_data = self.workout_data.copy()
        invalid_data["duration"] = -5
        response = self.client.post("/workouts/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("duration", response.data)

    def test_retrieve_other_user_workout(self):
        """Test retrieving another user's workout"""
        other_workout = Workout.objects.create(
            owner=self.other_user, title="Other Run", workout_type="cardio", duration=40, intensity="low"
        )
        response = self.client.get(f"/workouts/{other_workout.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_workout(self):
        """Ensure users cannot update workouts they do not own"""
        other_workout = Workout.objects.create(
            owner=self.other_user, title="Evening Run", workout_type="strength", duration=45, intensity="high"
        )
        response = self.client.patch(f"/workouts/{other_workout.id}/", {"title": "Unauthorized Update"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user_workout(self):
        """Ensure users cannot delete workouts they do not own"""
        other_workout = Workout.objects.create(
            owner=self.other_user, title="Evening Run", workout_type="strength", duration=45, intensity="high"
        )
        response = self.client.delete(f"/workouts/{other_workout.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_workout(self):
        """Test deleting a workout"""
        response = self.client.delete(f"/workouts/{self.workout.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Workout.objects.filter(id=self.workout.id).exists())

    def test_workout_statistics_multiple_workouts(self):
        """Test statistics endpoint with multiple workouts"""
        Workout.objects.create(
            owner=self.user, title="Evening Run", workout_type="strength", duration=45, intensity="high"
        )
        response = self.client.get("/workouts/statistics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_workouts"], 2)
        self.assertEqual(response.data["total_duration"], 75)

    def test_workout_statistics_other_user(self):
        """Ensure workout statistics endpoint returns data only for the authenticated user"""
        Workout.objects.create(
            owner=self.other_user, title="Other Run", workout_type="cardio", duration=50, intensity="low"
        )
        response = self.client.get("/workouts/statistics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_workouts"], 1)
        self.assertEqual(response.data["total_duration"], 30)

    def test_create_workout_maximum_duration(self):
        """Test creating a workout with the maximum allowed duration"""
        max_duration_data = self.workout_data.copy()
        max_duration_data["duration"] = 1440
        response = self.client.post("/workouts/", max_duration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["duration"], 1440)

    def test_edit_workout_as_owner(self):
        """Ensure owners can edit their workouts"""
        response = self.client.patch(f"/workouts/{self.workout.id}/", {"title": "Updated Run"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Run")

    def test_owner_workout_visibility_only(self):
        """Ensure the workout list only shows workouts for the authenticated user"""
        Workout.objects.create(
            owner=self.other_user, title="Other Run", workout_type="cardio", duration=50, intensity="low"
        )
        response = self.client.get("/workouts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["owner"], self.user.username)
