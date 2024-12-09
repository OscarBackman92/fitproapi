from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile
from django.utils import timezone
from workouts.models import Workout
from followers.models import Follower
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class ProfileTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def create_workout(self, user, date_logged=None):
        """Helper method to create a workout"""
        return Workout.objects.create(
            owner=user,
            title="Test Workout",
            workout_type="cardio",
            duration=30,
            intensity="moderate",
            date_logged=date_logged or timezone.now().date()
        )

    def test_profile_auto_creation(self):
        """Test that profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(Profile.objects.count(), 2)  # Both test users should have profiles

    def test_profile_list(self):
        """Test listing all profiles"""
        response = self.client.get('/profiles/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_profile_detail(self):
        """Test retrieving a specific profile"""
        response = self.client.get(f'/profiles/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')

    def test_profile_update(self):
        """Test updating profile"""
        data = {
            'name': 'Updated Name',
            'bio': 'Updated bio',
            'is_private': True
        }
        response = self.client.patch(
            f'/profiles/profiles/{self.user.profile.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['bio'], 'Updated bio')
        self.assertTrue(response.data['is_private'])

    def test_unauthorized_profile_update(self):
        """Test that users cannot update other users' profiles"""
        data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            f'/profiles/profiles/{self.user2.profile.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_image_upload(self):
        """Test profile image upload"""
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        response = self.client.patch(
            f'/profiles/profiles/{self.user.profile.id}/',
            {'image': image},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)

    def test_profile_statistics(self):
        """Test profile statistics endpoint"""
        # Create some workouts with consecutive days
        today = timezone.now().date()
        for i in range(3):
            self.create_workout(
                self.user,
                date_logged=today - datetime.timedelta(days=i)
            )

        # Create a workout with a gap to test streak
        self.create_workout(
            self.user,
            date_logged=today - datetime.timedelta(days=5)
        )

        response = self.client.get(f'/profiles/profiles/{self.user.profile.id}/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_workouts'], 4)
        self.assertEqual(response.data['current_streak'], 3)
        self.assertEqual(response.data['total_duration'], 120)  # 4 workouts * 30 minutes

    def test_current_user_profile(self):
        """Test getting current user's profile"""
        response = self.client.get('/profiles/profiles/current/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)

    def test_profile_followers_count(self):
        """Test followers count in profile"""
        # Create a follower relationship
        Follower.objects.create(follower=self.user2, followed=self.user)
        
        response = self.client.get(f'/profiles/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)

    def test_private_profile(self):
        """Test private profile functionality"""
        # Make profile private
        self.user.profile.is_private = True
        self.user.profile.save()

        # Logout current user and login as user2
        self.client.logout()
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(f'/profiles/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should still see basic info but not detailed stats
        self.assertEqual(response.data['owner'], 'testuser')
        self.assertTrue(response.data['is_private'])

    def test_profile_stats_no_workouts(self):
        """Test profile statistics with no workouts"""
        response = self.client.get(f'/profiles/profiles/{self.user.profile.id}/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_workouts'], 0)
        self.assertEqual(response.data['current_streak'], 0)
        self.assertEqual(response.data['total_duration'], 0)

    def test_profile_not_found(self):
        """Test accessing non-existent profile"""
        response = self.client.get('/profiles/profiles/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_stats_not_found(self):
        """Test accessing non-existent profile statistics"""
        response = self.client.get('/profiles/profiles/99999/statistics/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)