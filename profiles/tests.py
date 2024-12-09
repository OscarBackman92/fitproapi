from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile
from django.urls import reverse
from followers.models import Follower

class ProfileTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        # Force authentication with first user
        self.client.force_authenticate(user=self.user)

    def test_profile_auto_creation(self):
        """Test that profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(Profile.objects.count(), 2)
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(str(profile), f"{self.user}'s profile (ID: {profile.id})")

    def test_profile_list(self):
        """Test listing all profiles"""
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['owner'], self.user2.username)  # Updated
        self.assertEqual(response.data[1]['owner'], self.user.username)   # Updated


    def test_profile_detail(self):
        """Test retrieving a specific profile"""
        response = self.client.get(
            reverse('profile-detail', kwargs={'pk': self.user.profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')
        self.assertTrue(response.data['is_owner'])

    def test_profile_update_owner(self):
        """Test updating own profile"""
        update_data = {
            'name': 'Updated Name',
            'content': 'Updated content'
        }
        response = self.client.patch(
            reverse('profile-detail', kwargs={'pk': self.user.profile.id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['content'], 'Updated content')

    def test_profile_update_non_owner(self):
        """Test that users cannot update other users' profiles"""
        self.client.force_authenticate(user=self.user2)
        update_data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'pk': self.user.profile.id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_followers_count(self):
        """Test followers count in profile"""
        # Create a follower relationship
        Follower.objects.create(
            follower=self.user2,
            followed=self.user
        )
        
        response = self.client.get(
            reverse('profile-detail', kwargs={'pk': self.user.profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)

    def test_current_user_profile(self):
        """Test getting current user's profile"""
        response = self.client.get(reverse('current-user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertTrue(response.data['is_owner'])

    def test_profile_not_found(self):
        """Test accessing non-existent profile"""
        response = self.client.get(
            reverse('profile-detail', kwargs={'pk': 999999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Test unauthenticated access to profiles"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Updated

    def test_following_id_present(self):
        """Test following_id is present in response when following a user"""
        # Create a follower relationship
        follower = Follower.objects.create(
            follower=self.user,
            followed=self.user2
        )
        
        response = self.client.get(
            reverse('profile-detail', kwargs={'pk': self.user2.profile.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_id'], follower.id)