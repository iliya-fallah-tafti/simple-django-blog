"""
URL configuration for Final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from django.contrib import admin
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from blog.sitemaps import BlogSitemap
from main.sitemaps import StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static
from main.views import *

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', coming_soon_view, name='coming_soon_root'),
    # path('<path:unknown_path>', coming_soon_view, name='coming_soon_catch_all'),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('captcha/', include('captcha.urls')),
    path('blog/', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
