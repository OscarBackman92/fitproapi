from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route


urlpatterns = [
    path('', root_route, name='root'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include(
        'dj_rest_auth.registration.urls')),

    # API endpoints
    path('api/workouts/', include('workouts.urls')),
    path('api/posts/', include('workoutposts.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/likes/', include('likes.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/followers/', include('followers.urls')),
]
