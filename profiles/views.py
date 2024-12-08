from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
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
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        try:
            profile_id = self.kwargs.get('pk')
            
            # If no profile_id is provided, return the current user's profile
            if not profile_id and self.request.user.is_authenticated:
                return self.request.user.profile
                
            profile = get_object_or_404(Profile, id=profile_id)
            self.check_object_permissions(self.request, profile)
            return profile
            
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        return Profile.objects.all().select_related('owner')

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