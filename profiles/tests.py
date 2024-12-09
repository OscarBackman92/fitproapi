from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from profiles.models import Profile
from followers.models import Follower
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_retrieve_profile(self):
        response = self.client.get(f'/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], self.user.username)

    def test_update_profile(self):
        response = self.client.patch(f'/profiles/{self.user.profile.id}/', {'name': 'Updated Name'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_unauthorized_profile_update(self):
        self.client.logout()  # Simulate an unauthorized user
        response = self.client.patch(f'/profiles/{self.user.profile.id}/', {'name': 'Unauthorized'})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_profile_auto_creation_on_signup(self):
        new_user = User.objects.create_user(username='newuser', password='testpass123')
        self.assertTrue(Profile.objects.filter(owner=new_user).exists())

    def test_retrieve_non_existent_profile(self):
        response = self.client.get('/profiles/999/')  # ID 999 likely does not exist
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_followers_and_following_counts(self):
        user2 = User.objects.create_user(username='user2', password='testpass123')
        Follower.objects.create(follower=self.user, followed=user2)

        response = self.client.get(f'/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['following_count'], 1)
        self.assertEqual(response.data['followers_count'], 0)

        response = self.client.get(f'/profiles/{user2.profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['followers_count'], 1)
        self.assertEqual(response.data['following_count'], 0)

    def test_profile_edit_by_non_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='testpass123')
        self.client.force_authenticate(user=another_user)

        response = self.client.patch(f'/profiles/{self.user.profile.id}/', {'name': 'Hacked'})
        self.assertEqual(response.status_code, 403)  # Forbidden
