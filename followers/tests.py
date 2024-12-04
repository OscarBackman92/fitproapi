from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Follower

class FollowerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        response = self.client.post('/api/followers/followers/', {
            'follower': self.user1.id,
            'followed': self.user2.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unfollow_user(self):
        follow = Follower.objects.create(follower=self.user1, followed=self.user2)
        response = self.client.delete(f'/api/followers/followers/{follow.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
