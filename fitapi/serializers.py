from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

class CurrentUserSerializer(UserDetailsSerializer):
    pk = serializers.ReadOnlyField(source='id')
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'profile_id': obj.profile.id,
                'profile_image': obj.profile.image.url if obj.profile.image else None,
            }
        return None

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'pk', 'username', 'profile'
        )
