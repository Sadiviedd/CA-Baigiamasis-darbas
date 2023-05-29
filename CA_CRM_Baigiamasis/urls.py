from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Projects.urls", namespace="projects")),
    path('', include('users.urls')),
]
