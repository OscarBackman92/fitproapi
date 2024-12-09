from django.contrib import admin
from .models import Workout

# Register your models here.
admin.site.register(Workout)
list = [ 'id', 'name', 'date', 'distance', 'time', 'description']