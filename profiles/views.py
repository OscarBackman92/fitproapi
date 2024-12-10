from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from .models import Profile
from .serializers import ProfileSerializer
from fitapi.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.annotate(
            posts_count=Count('owner__workout_posts', distinct=True),
            followers_count=Count('owner__followers', distinct=True),
            following_count=Count('owner__following', distinct=True)
        ).order_by('-created_at')


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'owner'  # Use 'owner' as the lookup field instead of 'id'

    def get_queryset(self):
        return Profile.objects.annotate(
            posts_count=Count('owner__workout_posts', distinct=True),
            followers_count=Count('owner__followers', distinct=True),
            following_count=Count('owner__following', distinct=True)
        )


class CurrentUserProfile(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = Profile.objects.annotate(
            posts_count=Count('owner__workout_posts', distinct=True),
            followers_count=Count('owner__followers', distinct=True),
            following_count=Count('owner__following', distinct=True)
        )
        return get_object_or_404(queryset, owner=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_statistics(request, owner):
    """Get statistics for a specific profile"""
    profile = get_object_or_404(Profile, owner=owner)  # Lookup by owner
    workouts = profile.owner.workouts.all()

    stats = {
        'total_workouts': workouts.count(),
        'total_duration': sum(w.duration for w in workouts),
        'current_streak': 0  # Implement streak calculation logic here
    }

    return Response(stats)
