"""SarayuLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from calendar_schedule.views import register_user, login_user, logout_user, list_events, add_event, delete_event, \
    edit_event

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('events/list/', list_events),
    path('events/add/', add_event),
    path('events/delete/', delete_event),
    path('events/edit/', edit_event),
]
