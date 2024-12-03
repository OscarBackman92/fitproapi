from rest_framework import serializers
from .models import WorkoutPost
from likes.models import Like
from comments.models import Comment

class WorkoutPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField(source='likes.count')
    comments_count = serializers.ReadOnlyField(source='comments.count')

    class Meta:
        model = WorkoutPost
        fields = ['id', 'user', 'workout', 'content', 'created_at', 'likes_count', 'comments_count']
