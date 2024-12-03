from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Follower
from .serializers import FollowerSerializer
from django.contrib.auth.models import User

class FollowerListView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class UserFollowerListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following = Follower.objects.filter(follower=user)
        return following
