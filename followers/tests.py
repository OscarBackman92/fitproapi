from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Follower


class FollowerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.user_to_follow = User.objects.create_user(
            username='followuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_follow_user(self):
        response = self.client.post('/api/followers/followers/', {
            'followed': self.user_to_follow.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unfollow_user(self):
        follower = Follower.objects.create(
            follower=self.user,
            followed=self.user_to_follow
        )
        response = self.client.delete(
            f'/api/followers/followers/{follower.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
