from rest_framework import serializers
from .models import Profile
from followers.models import Follower  # Ensure correct import of Follower model

class ProfileSerializer(serializers.ModelSerializer):
    # Read-only fields
    owner = serializers.ReadOnlyField(source='owner.username')
    posts_count = serializers.ReadOnlyField()  # Handled in the view (via annotate)
    followers_count = serializers.ReadOnlyField()  # Handled in the view (via annotate)
    following_count = serializers.ReadOnlyField()  # Handled in the view (via annotate)

    # Serializer method fields
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    # Get the current user's ownership status of the profile
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Get the ID of the 'Follower' object if the current user follows the profile owner
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
