from django.urls import path
from .views import FollowerListView, FollowerDetailView

urlpatterns = [
    path('followers/', FollowerListView.as_view()),
    path('followers/<int:pk>/', FollowerDetailView.as_view()),
]
