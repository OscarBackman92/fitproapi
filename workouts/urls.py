from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutList.as_view(), name='workout-list'),
    path('<int:pk>/', views.WorkoutDetail.as_view(), name='workout-detail'),
    path('statistics/<int:user_id>/', views.workout_statistics, name='workout-statistics'),
]