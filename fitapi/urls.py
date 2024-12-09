from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route

urlpatterns = [
    path('', root_route, name='root'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', logout_route),
    path('profiles/', include('profiles.urls')),
    path('workouts/', include('workouts.urls')),
    path('posts/', include('workoutposts.urls')),
    path('likes/', include('likes.urls')),
    path('comments/', include('comments.urls')),
    path('followers/', include('followers.urls')),
    
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
