from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile-list'),
    path('current/', views.CurrentUserProfile.as_view(), name='current-user-profile'),
    path('<int:owner>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('<int:owner>/statistics/', views.profile_statistics, name='profile-statistics'),
]