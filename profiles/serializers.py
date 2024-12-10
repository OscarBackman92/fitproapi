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
        """
        Returns whether the current user is the owner of this profile.
        """
        request = self.context.get('request')
        return request and request.user == obj.owner

    def get_following_id(self, obj):
        """
        Returns the ID of the follow relationship if the current user is following the profile's owner.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            following = request.user.following.filter(
                followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
        read_only_fields = ['created_at', 'updated_at', 'posts_count', 'followers_count', 'following_count']
