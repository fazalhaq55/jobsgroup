"""django_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from jobs.models import Info
from django_main.sitemap import StaticViewSitemap

app_name = "jobs"

sitemaps = {
    
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('', include('front_end.urls')),
    path('jobs/', include('jobs.urls')),
    # path('user/', include('Employer.urls')),
    path('scholarships/', include('scholarship.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('User.urls')),
    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
