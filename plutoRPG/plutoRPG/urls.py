"""
URL configuration for plutoRPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from homepage.views import index
from play.views import game
from worldmap.views import worldmap
from monsters.views import monsters
from classes.views import classes
from equipment.views import equipment
from login.views import LoginView, page_logout
from patch_notes.views import patch_notes
from dev_logs.views import dev_logs
from quests.views import quests
from characters.views import character_manager

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="homepage"),
    path('play/', game),
    path('worldmap/', worldmap),
    path('monsters/', monsters),
    path('classes/', classes),
    path('equipment/', equipment),
    path('login/', LoginView.as_view()),
    path('patchnotes/', patch_notes),
    path('devlogs/', dev_logs),
    path('quests/', quests),
    path('logout/', page_logout),
    path('character_manager/', character_manager),
]
