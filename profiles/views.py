from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Profile
from .serializers import ProfileSerializer
from fitapi.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

def calculate_streak(workouts):
    """
    Calculate the current workout streak.
    A streak is maintained by working out on consecutive days.
    """
    if not workouts.exists():
        return 0

    workout_dates = workouts.values_list(
        'date_logged', flat=True
    ).order_by('-date_logged')
    
    dates = list(workout_dates)
    
    if not dates:
        return 0

    streak = 1
    current_date = dates[0]
    
    for next_date in dates[1:]:
        date_diff = (current_date - next_date).days
        
        if date_diff == 1:
            streak += 1
            current_date = next_date
        elif date_diff == 0:
            current_date = next_date
            continue
        else:
            break
    
    return streak

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.annotate(
            posts_count=Count('owner__workout_posts', distinct=True),
            followers_count=Count('owner__followers', distinct=True),
            following_count=Count('owner__following', distinct=True)
        ).order_by('-created_at')

class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        return Profile.objects.annotate(
            posts_count=Count('owner__workout_posts', distinct=True),
            followers_count=Count('owner__followers', distinct=True),
            following_count=Count('owner__following', distinct=True)
        )

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'current':
            return get_object_or_404(self.get_queryset(), owner=self.request.user)
        return get_object_or_404(self.get_queryset(), pk=pk)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_statistics(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
        workouts = profile.owner.workouts.all()
        
        stats = {
            'total_workouts': workouts.count(),
            'workouts_this_week': workouts.filter(
                date_logged__gte=timezone.now() - timezone.timedelta(days=7)
            ).count(),
            'total_duration': workouts.aggregate(Sum('duration'))['duration__sum'] or 0,
            'current_streak': calculate_streak(workouts),
        }
        
        return Response(stats)
    except Profile.DoesNotExist:
        return Response(
            {'detail': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )