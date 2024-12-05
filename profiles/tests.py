from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.profile = Profile.objects.get(owner=self.user)

    def test_profile_creation(self):
        self.assertTrue(Profile.objects.filter(owner=self.user).exists())

    def test_profile_update(self):
        response = self.client.patch(
            f'/api/profiles/profiles/{self.profile.id}/',
            {'name': 'Updated Name', 'content': 'New bio'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
