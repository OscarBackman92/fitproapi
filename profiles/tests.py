from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
        self.profile = Profile.objects.get(owner=self.user)

    def test_profile_auto_creation(self):
        self.assertTrue(Profile.objects.filter(owner=self.user).exists())

    def test_get_profile_list(self):
        response = self.client.get('/api/profiles/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_own_profile(self):
        response = self.client.put(
            f'/api/profiles/profiles/{self.profile.id}/',
            {
                'name': 'Updated Name',
                'content': 'New bio'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, 'Updated Name')

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()