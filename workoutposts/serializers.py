from rest_framework import serializers
from .models import WorkoutPost
from likes.models import Like

class WorkoutPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    workout_type = serializers.ReadOnlyField(source='workout.workout_type')
    workout_duration = serializers.ReadOnlyField(source='workout.duration')
    workout_intensity = serializers.ReadOnlyField(source='workout.intensity')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                user=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = WorkoutPost
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'workout', 'workout_type', 'workout_duration',
            'workout_intensity', 'content',
            'like_id', 'likes_count', 'comments_count',
        ]
