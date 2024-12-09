from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('followers_count', response.data[0])

    def test_retrieve_profile(self):
        response = self.client.get(f'/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)

    def test_update_profile(self):
        response = self.client.patch(f'/profiles/{self.user.profile.id}/', {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
