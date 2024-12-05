from rest_framework import generics, permissions
from django.db.models import Count
from .models import WorkoutPost
from .serializers import WorkoutPostSerializer
from fitapi.permissions import IsOwnerOrReadOnly

class WorkoutPostList(generics.ListCreateAPIView):
    serializer_class = WorkoutPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = WorkoutPost.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        ).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WorkoutPostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = WorkoutPostSerializer
    queryset = WorkoutPost.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )