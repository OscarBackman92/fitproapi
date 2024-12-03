from django.urls import path
from .views import CommentList

urlpatterns = [
    path('comments/', CommentList.as_view(), name='comment-list'),
]
