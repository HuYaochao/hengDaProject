"""
URL configuration for hengDaProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from homeApp.views import home



urlpatterns = [
    path("admin/", admin.site.urls),
    path('aboutApp/',include("aboutApp.urls")),
    path('contactApp/',include("contactApp.urls")),
    path('newsApp/',include("newsApp.urls")),
    path('productsApp/',include("productsApp.urls")),
    path('scienceApp/',include("scienceApp.urls")),
    path('serviceApp/',include("serviceApp.urls")),
    path("",home,name='home'),
    path('ueditor/',include('DjangoUeditor.urls')),
    path('search/',include('haystack.urls'))
    
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)