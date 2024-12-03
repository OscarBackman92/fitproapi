from django.urls import path
from .views import WorkoutPostList

urlpatterns = [
    path('posts/', WorkoutPostList.as_view(), name='workoutpost-list'),
]
