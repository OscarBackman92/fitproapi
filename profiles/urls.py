from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile-list'),
    path('current/', views.ProfileDetail.as_view(), kwargs={'pk': 'current'}, name='current-user-profile'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('<int:pk>/statistics/', views.profile_statistics, name='profile-statistics'),
]