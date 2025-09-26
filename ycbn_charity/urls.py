# URL configuration for ycbn_charity project.
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from charity.sitemaps import sitemaps
from django.views.generic import TemplateView

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    # Include Django auth URLs without a namespace so names like 'login'/'logout' resolve
    path('accounts/', include('django.contrib.auth.urls')),
    # Main app URLs
    path('', include('charity.urls')),
    # SEO: sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # SEO: robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]
