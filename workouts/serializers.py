from rest_framework import serializers
from .models import Workout
from workoutposts.models import WorkoutPost
from likes.models import Like

class WorkoutSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    profile_image = serializers.ReadOnlyField(source='user.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            post = WorkoutPost.objects.filter(workout=obj).first()
            if post:
                like = Like.objects.filter(user=user, post=post).first()
                return like.id if like else None
        return None

    class Meta:
        model = Workout
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'workout_type', 'date_logged', 'duration',
            'intensity', 'notes', 'likes_count', 'comments_count',
            'like_id',
        ]