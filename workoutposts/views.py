from rest_framework import generics
from .models import WorkoutPost
from .serializers import WorkoutPostSerializer

class WorkoutPostList(generics.ListCreateAPIView):
    queryset = WorkoutPost.objects.all()
    serializer_class = WorkoutPostSerializer
