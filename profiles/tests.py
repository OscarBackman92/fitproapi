from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from profiles.models import Profile
from followers.models import Follower
import json

class ProfileTests(APITestCase):
    def setUp(self):
        """
        Set up test data - create test users and authenticate
        """
        self.client = APIClient()
        # Create main test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        # Create secondary test user
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )
        # Create a third user for following tests
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='testpass123',
            email='test3@example.com'
        )
        # Authenticate as main test user
        self.client.force_authenticate(user=self.user)

    def test_profile_auto_creation(self):
        """Test profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(Profile.objects.count(), 3)  # Should have 3 profiles
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(str(profile), f"{self.user}'s profile")
        # Check default values
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
        self.assertEqual(profile.image, 'images/default_profile_ylwpgw.png')

    def test_profile_list(self):
        """Test retrieving profile list"""
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should show all profiles
        # Check response structure
        self.assertIn('owner', response.data[0])
        self.assertIn('created_at', response.data[0])
        self.assertIn('image', response.data[0])
        # Verify ordering (should be by created_at descending)
        self.assertEqual(response.data[0]['owner'], self.user3.username)
        self.assertEqual(response.data[2]['owner'], self.user.username)

    def test_profile_detail(self):
        """Test retrieving individual profile details"""
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')
        self.assertTrue(response.data['is_owner'])
        # Check all profile fields are present
        expected_fields = {
            'owner', 'created_at', 'updated_at', 'name', 
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count'
        }
        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_profile_update_owner(self):
        """Test updating profile by owner"""
        update_data = {
            'name': 'Updated Name',
            'content': 'Updated content',
        }
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.username}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['content'], 'Updated content')
        # Verify database was updated
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(profile.name, 'Updated Name')
        self.assertEqual(profile.content, 'Updated content')

    def test_profile_update_non_owner(self):
        """Test attempting to update profile by non-owner"""
        self.client.force_authenticate(user=self.user2)
        update_data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.username}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify profile wasn't changed
        profile = Profile.objects.get(owner=self.user)
        self.assertNotEqual(profile.name, 'Unauthorized Update')

    def test_profile_update_invalid_data(self):
        """Test updating profile with invalid data"""
        # Test with name too long
        update_data = {'name': 'x' * 256}  # Max length is 255
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.username}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_profile_followers_count(self):
        """Test follower count functionality"""
        # Create some follows
        Follower.objects.create(follower=self.user2, followed=self.user)
        Follower.objects.create(follower=self.user3, followed=self.user)
        
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 2)
        self.assertEqual(response.data['following_count'], 0)

    def test_current_user_profile(self):
        """Test retrieving current user's profile"""
        response = self.client.get(reverse('current-user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertTrue(response.data['is_owner'])
        # Should include all profile data
        self.assertIn('name', response.data)
        self.assertIn('content', response.data)
        self.assertIn('image', response.data)

    def test_profile_not_found(self):
        """Test requesting non-existent profile"""
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': 'nonexistentuser'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Test accessing profiles while not authenticated"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_following_id_present(self):
        """Test following_id field in profile response"""
        # Create a follow relationship
        follower = Follower.objects.create(
            follower=self.user,
            followed=self.user2
        )
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user2.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_id'], follower.id)

    def test_profile_statistics(self):
        """Test profile statistics endpoint"""
        response = self.client.get(
            reverse('profile-statistics', kwargs={'owner': self.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_workouts', response.data)
        self.assertIn('total_duration', response.data)
        self.assertIn('current_streak', response.data)

    def tearDown(self):
        """Clean up after tests"""
        User.objects.all().delete()
        Profile.objects.all().delete()
        Follower.objects.all().delete()