from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Profile
from followers.models import Follower

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_profile_detail(self):
        """Test retrieving individual profile details"""
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')
        self.assertTrue(response.data['is_owner'])

    def test_profile_update_owner(self):
        """Test updating profile by owner"""
        update_data = {'name': 'Updated Name', 'content': 'Updated content'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['content'], 'Updated content')

    def test_profile_update_non_owner(self):
        """Test attempting to update profile by non-owner"""
        self.client.force_authenticate(user=self.user2)
        update_data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_followers_count(self):
        """Test follower count functionality"""
        Follower.objects.create(follower=self.user2, followed=self.user)
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)

    def test_profile_statistics(self):
        """Test profile statistics endpoint"""
        response = self.client.get(
            reverse('profile-statistics', kwargs={'owner': self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_workouts', response.data)
        self.assertIn('total_duration', response.data)

    def test_following_id_present(self):
        """Test following_id field in profile response"""
        follower = Follower.objects.create(follower=self.user, followed=self.user2)
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_id'], follower.id)