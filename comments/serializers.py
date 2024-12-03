from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    workout_post = serializers.ReadOnlyField(source='post.workout.title')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'workout_post', 'content', 'created_at']