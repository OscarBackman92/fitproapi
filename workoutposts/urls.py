from django.urls import path
from workoutposts import views

urlpatterns = [
    path('', views.WorkoutPostList.as_view(), name='workoutpost-list'),
]
