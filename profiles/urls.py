from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/me/', views.CurrentUserProfile.as_view()),  # Add this line
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]