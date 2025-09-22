# URL configuration for ycbn_charity project.
from django.contrib import admin
from django.urls import path, include

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    # Include Django auth URLs without a namespace so names like 'login'/'logout' resolve
    path('accounts/', include('django.contrib.auth.urls')),
    # Main app URLs
    path('', include('charity.urls')),
]
