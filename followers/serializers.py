from rest_framework import serializers
from .models import Follower
from django.contrib.auth.models import User


class FollowerSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed', 'created_at']


class UserFollowerSerializer(serializers.ModelSerializer):
    followers = FollowerSerializer(many=True, read_only=True)
    following = FollowerSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followers', 'following']
