from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile
from django.urls import reverse
from followers.models import Follower

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_profile_auto_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(Profile.objects.count(), 2)
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(str(profile), f"{self.user}'s profile")

    def test_profile_list(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['owner'], self.user2.username)
        self.assertEqual(response.data[1]['owner'], self.user.username)

    def test_profile_detail(self):
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')
        self.assertTrue(response.data['is_owner'])

    def test_profile_update_owner(self):
        update_data = {'name': 'Updated Name', 'content': 'Updated content'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.username}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['content'], 'Updated content')

    def test_profile_update_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        update_data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('profile-detail', kwargs={'owner': self.user.username}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_followers_count(self):
        Follower.objects.create(follower=self.user2, followed=self.user)
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)

    def test_current_user_profile(self):
        response = self.client.get(reverse('current-user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertTrue(response.data['is_owner'])

    def test_profile_not_found(self):
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': 'nonexistentuser'})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_following_id_present(self):
        follower = Follower.objects.create(follower=self.user, followed=self.user2)
        response = self.client.get(
            reverse('profile-detail', kwargs={'owner': self.user2.username})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_id'], follower.id)
