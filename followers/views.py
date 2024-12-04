from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated 
from .models import Follower
from .serializers import FollowerSerializer

class FollowerListView(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        followed_id = self.request.data.get('followed')
        if followed_id:
            serializer.save(follower=self.request.user)

class FollowerDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer