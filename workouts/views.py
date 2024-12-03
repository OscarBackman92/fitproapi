
from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from fitapi.permissions import IsOwnerOrReadOnly
from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutList(generics.ListCreateAPIView):
    """
    List all workouts or create a workout if logged in.
    The perform_create method associates the workout with the logged-in user.
    """
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Workout.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-date_logged')
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = [
        'workout_type',
        'intensity',
        'user__profile',
    ]
    
    search_fields = [
        'title',
        'user__username',
        'notes',
    ]
    
    ordering_fields = [
        'likes_count',
        'comments_count',
        'date_logged',
        'intensity',
    ]

    def perform_create(self, serializer):
        """Associates the workout with the logged-in user."""
        serializer.save(user=self.request.user)


class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a workout, or edit/delete it if you own it.
    """
    serializer_class = WorkoutSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Workout.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-date_logged')
