from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Workout
from .serializers import WorkoutSerializer
from fitapi.permissions import IsOwnerOrReadOnly

class WorkoutList(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Workout.objects.all()
        owner = self.request.query_params.get('owner', None)
        
        if owner is not None:
            queryset = queryset.filter(owner_id=owner)
        else:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(owner=self.request.user)
            else:
                queryset = queryset.none()

        workout_type = self.request.query_params.get('workout_type', None)
        if workout_type:
            queryset = queryset.filter(workout_type=workout_type)
            
        intensity = self.request.query_params.get('intensity', None)
        if intensity:
            queryset = queryset.filter(intensity=intensity)
            
        return queryset.order_by('-date_logged')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def workout_statistics(request):
    """
    Get workout statistics for the authenticated user
    """
    try:
        workouts = Workout.objects.filter(owner=request.user)
        
        # Calculate basic stats
        total_workouts = workouts.count()
        total_duration = workouts.aggregate(Sum('duration'))['duration__sum'] or 0
        
        # Calculate workouts this week
        week_start = timezone.now().date() - timezone.timedelta(days=7)
        workouts_this_week = workouts.filter(date_logged__gte=week_start).count()
        
        # Calculate streak
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
            
        # Get workout types distribution
        workout_types = workouts.values('workout_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get monthly trends
        monthly_stats = workouts.extra(
            select={'month': "DATE_TRUNC('month', date_logged)"}
        ).values('month').annotate(
            total=Count('id'),
            duration=Sum('duration')
        ).order_by('-month')[:12]
        
        stats = {
            'total_workouts': total_workouts,
            'workouts_this_week': workouts_this_week,
            'current_streak': streak,
            'total_duration': total_duration,
            'workout_types': list(workout_types),
            'monthly_trends': list(monthly_stats)
        }
        
        return Response(stats)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )