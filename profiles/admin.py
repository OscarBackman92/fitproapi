from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'created_at', 'updated_at')
    search_fields = ('owner__username', 'name', 'content')
    list_filter = ('created_at', 'updated_at')