from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.db.models import Count
from .models import Profile
from .serializers import ProfileSerializer
from fitapi.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    The current user's ID is automatically available in request.user.id
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),
        followers_count=Count('owner__followers', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile.
    The URL parameter 'pk' matches to the user's ID
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),
        followers_count=Count('owner__followers', distinct=True),
        following_count=Count('owner__following', distinct=True)
    )
    serializer_class = ProfileSerializer

class CurrentUserProfile(generics.RetrieveAPIView):
    """
    Retrieve the current user's profile.
    Uses the authenticated user's ID from the request.
    """
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