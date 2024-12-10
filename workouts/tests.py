from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from workouts.models import Workout
from django.utils import timezone
import json

class WorkoutTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        # Authenticate main test user
        self.client.force_authenticate(user=self.user)

        # Create a test workout
        self.workout_data = {
            "title": "Morning Run",
            "workout_type": "cardio",
            "duration": 30,
            "intensity": "moderate",
            "notes": "Good pace",
            "date_logged": timezone.now().date().isoformat()
        }
        self.workout = Workout.objects.create(
            owner=self.user,
            **self.workout_data
        )

    def test_create_workout(self):
        """Test creating a new workout"""
        new_workout_data = {
            "title": "Evening Yoga",
            "workout_type": "flexibility",
            "duration": 45,
            "intensity": "low",
            "notes": "Relaxing session",
            "date_logged": timezone.now().date().isoformat()
        }
        response = self.client.post(
            reverse('workout-list'),
            new_workout_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Evening Yoga')
        self.assertEqual(response.data['owner'], 'testuser')

    def test_list_workouts(self):
        """Test listing workouts"""
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Morning Run')

    def test_get_workout_detail(self):
        """Test retrieving a specific workout"""
        response = self.client.get(
            reverse('workout-detail', kwargs={'pk': self.workout.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Morning Run')
        self.assertEqual(response.data['duration'], 30)

    def test_update_workout(self):
        """Test updating a workout"""
        update_data = {
            "title": "Updated Run",
            "duration": 35
        }
        response = self.client.patch(
            reverse('workout-detail', kwargs={'pk': self.workout.id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Run')
        self.assertEqual(response.data['duration'], 35)

    def test_delete_workout(self):
        """Test deleting a workout"""
        response = self.client.delete(
            reverse('workout-detail', kwargs={'pk': self.workout.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workout.objects.count(), 0)

    def test_workout_invalid_duration(self):
        """Test creating workout with invalid duration"""
        invalid_data = self.workout_data.copy()
        invalid_data['duration'] = -5
        response = self.client.post(
            reverse('workout-list'),
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('duration', response.data)

    def test_workout_statistics(self):
        """Test workout statistics endpoint"""
        # Create additional workout for statistics
        Workout.objects.create(
            owner=self.user,
            title="Evening Run",
            workout_type="cardio",
            duration=45,
            intensity="high"
        )
        
        response = self.client.get(reverse('workout-statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_workouts'], 2)
        self.assertEqual(response.data['total_duration'], 75)
        self.assertIn('workout_types', response.data)
        self.assertIn('monthly_trends', response.data)

    def test_unauthorized_workout_access(self):
        """Test unauthorized workout access"""
        # Create workout for other user
        other_workout = Workout.objects.create(
            owner=self.other_user,
            title="Other's Workout",
            workout_type="strength",
            duration=40,
            intensity="high"
        )
        
        # Try to update other user's workout
        response = self.client.patch(
            reverse('workout-detail', kwargs={'pk': other_workout.id}),
            {"title": "Unauthorized Update"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Try to delete other user's workout
        response = self.client.delete(
            reverse('workout-detail', kwargs={'pk': other_workout.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workout_filtering(self):
        """Test workout filtering capabilities"""
        # Create workouts with different types
        Workout.objects.create(
            owner=self.user,
            title="Strength Training",
            workout_type="strength",
            duration=45,
            intensity="high"
        )
        
        # Test filtering by workout type
        response = self.client.get(f"{reverse('workout-list')}?workout_type=cardio")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['workout_type'], 'cardio')

    def tearDown(self):
        """Clean up after tests"""
        User.objects.all().delete()
        Workout.objects.all().delete()