from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            following = request.user.following.filter(
                followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size cannot exceed 2MB')
        return value

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'bio', 'image', 'is_owner', 'following_id',
            'weight', 'height', 'gender', 'date_of_birth',
            'posts_count', 'followers_count', 'following_count',
            'is_private'
        ]