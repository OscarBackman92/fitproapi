from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Count
from .models import Profile
from .serializers import ProfileSerializer
from fitapi.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),
        followers_count=Count('owner__followers', distinct=True),  
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),
        followers_count=Count('owner__followers', distinct=True),
        following_count=Count('owner__following', distinct=True)
    )
    serializer_class = ProfileSerializer

class CurrentUserProfile(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(
            Profile.objects.annotate(
                posts_count=Count('owner__workout_posts', distinct=True),
                followers_count=Count('owner__followers', distinct=True),
                following_count=Count('owner__following', distinct=True)
            ),
            owner=self.request.user
        )