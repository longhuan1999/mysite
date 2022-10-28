"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from chongzhi import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico',RedirectView.as_view(url='static/favicon.ico')),
    path('', views.index),
    path('chongzhi/', include('chongzhi.urls')),
    path('chaxun/', include('chaxun.urls')),
    path('admin/', admin.site.urls),
]
