from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Workout
from .serializers import WorkoutSerializer
from fitapi.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)

class WorkoutList(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return workouts for the authenticated user only.
        """
        return Workout.objects.filter(owner=self.request.user).order_by('-date_logged')

    def perform_create(self, serializer):
        """
        Restrict workout creation to the authenticated user.
        """
        serializer.save(owner=self.request.user)

class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific workout.
    Only the owner can update or delete.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        """
        Return all workouts for use with detail view.
        """
        return Workout.objects.all()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def workout_statistics(request):
    """
    Provide statistics for the authenticated user's workouts.
    Statistics include total workouts, weekly workouts, current streak,
    total duration, workout types distribution, and monthly trends.
    """
    try:
        workouts = Workout.objects.filter(owner=request.user)

        # Calculate total workouts and duration
        total_workouts = workouts.count()
        total_duration = workouts.aggregate(Sum('duration'))['duration__sum'] or 0

        # Calculate weekly workouts
        week_start = timezone.now().date() - timezone.timedelta(days=7)
        workouts_this_week = workouts.filter(date_logged__gte=week_start).count()

        # Calculate current streak
        streak = 0
        if total_workouts > 0:
            dates = workouts.values_list('date_logged', flat=True).order_by('-date_logged')
            current_date = dates[0]
            streak = 1
            for date in dates[1:]:
                if (current_date - date).days == 1:
                    streak += 1
                    current_date = date
                else:
                    break

        # Aggregate workout types
        workout_types = workouts.values('workout_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Aggregate monthly statistics
        monthly_stats = workouts.extra(
            select={'month': "DATE_TRUNC('month', date_logged)"}
        ).values('month').annotate(
            total=Count('id'),
            duration=Sum('duration')
        ).order_by('-month')[:12]

        # Compile statistics
        stats = {
            'total_workouts': total_workouts,
            'workouts_this_week': workouts_this_week,
            'current_streak': streak,
            'total_duration': total_duration,
            'workout_types': list(workout_types),
            'monthly_trends': list(monthly_stats),
        }

        return Response(stats)
    except Exception as e:
        logger.error(f"Error in workout_statistics: {str(e)}")
        return Response(
            {
                'total_workouts': 0,
                'workouts_this_week': 0,
                'current_streak': 0,
                'total_duration': 0,
                'workout_types': [],
                'monthly_trends': [],
            },
            status=status.HTTP_200_OK
        )
