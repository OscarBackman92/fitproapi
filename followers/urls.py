from django.urls import path
from .views import FollowerListView, UserFollowerListView

urlpatterns = [
    path('followers/', FollowerListView.as_view(), name='follower-list'),
    path('following/', UserFollowerListView.as_view(), name='following-list'),
]
