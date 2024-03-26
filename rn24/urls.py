"""
URL configuration for rn24 project.

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

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.static import serve

admin.sites.AdminSite.site_header = "RN24 backoffice"
admin.sites.AdminSite.site_title = "RN24 backoffice"
admin.sites.AdminSite.index_title = "RN24 backoffice"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", serve, {"document_root": settings.WHITENOISE_ROOT, "path": "index.html"}),
]
