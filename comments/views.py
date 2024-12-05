from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        serializer.save(user=self.request.user, post_id=post_id)
