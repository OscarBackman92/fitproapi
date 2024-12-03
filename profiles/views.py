from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from fitapi.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),  # Correct the field reference
        followers_count=Count('owner__followers', distinct=True),  # Correct the field reference
        following_count=Count('owner__following', distinct=True)  # Correct the field reference
    ).order_by('-created_at')  # Order by the profile's creation date
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile', 
        'owner__followers__owner__profile',      
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__date_joined',  # Use the user field for ordering
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__workout_posts', distinct=True),  # Correct the field reference
        followers_count=Count('owner__followers', distinct=True),  # Correct the field reference
        following_count=Count('owner__following', distinct=True)  # Correct the field reference
    ).order_by('-created_at')  # Order by the profile's creation date
    serializer_class = ProfileSerializer
