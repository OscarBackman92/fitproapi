from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from workoutposts.models import WorkoutPost
from workouts.models import Workout
from .models import Comment

class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.force_authenticate(user=self.user)
        
        self.workout = Workout.objects.create(
            user=self.user,
            title="Morning Run",
            workout_type="cardio",
            duration=30,
            intensity="moderate",
            date_logged="2024-03-14"
        )
        
        self.post = WorkoutPost.objects.create(
            user=self.user,
            workout=self.workout,
            content='Test post'
        )

    def test_create_comment(self):
        comment_data = {
            'post': self.post.id,
            'content': 'Great post!'
        }
        response = self.client.post('/api/comments/comments/', comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_list_comments(self):
        Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        response = self.client.get('/api/comments/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def tearDown(self):
        Comment.objects.all().delete()
        WorkoutPost.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()