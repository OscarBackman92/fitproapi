from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutList, WorkoutDetail

router = DefaultRouter()
router.register(r'workouts', WorkoutList)

urlpatterns = [
    path('', include(router.urls)),
    path('workouts/<int:pk>/', WorkoutDetail.as_view(), name='workout-detail'),
]
