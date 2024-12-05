from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from fitapi.permissions import IsOwnerOrReadOnly
from .models import Workout
from .serializers import WorkoutSerializer


class WorkoutList(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Workout.objects.all()

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'workout_type',
        'intensity',
        'owner__profile',
    ]

    search_fields = [
        'title',
        'owner__username',
        'notes',
    ]

    ordering_fields = [
        'date_logged',
        'intensity',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WorkoutSerializer
