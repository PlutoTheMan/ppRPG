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
from django.views.generic.base import RedirectView

from homepage.views import index
from play.views import game, get_characters, select_character, get_map_tile_sets
from worldmap.views import worldmap
from monsters.views import monsters
from classes.views import classes
from equipment.views import equipment
from login.views import LoginView, page_logout, RegisterView
from patch_notes.views import patch_notes
from dev_logs.views import dev_logs
from quests.views import quests
from notes.views import NotesView

from homepage.views import display_credits, download_credits_outfit

from characters.views import CharactersManagerView, DeleteCharacterView, GuildCreateView
from characters.views import view_character, view_all_characters

from guilds.views import view_guild, view_all_guilds, view_guild_members, ManageGuildView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('credits/', display_credits, name="credits"),
    path('credits/download', download_credits_outfit, name="credits_download"),
    path('', index, name="homepage"),
    path('play/', game, name="game"),
    path('worldmap/', worldmap, name="worldmap"),
    path('monsters/', monsters, name="monsters"),
    path('classes/', classes, name="classes"),
    path('equipment/', equipment, name="equipment"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('patchnotes/', patch_notes, name="patch_notes"),
    path('devlogs/', dev_logs, name="devlogs"),
    path('quests/', quests, name="quests"),
    path('logout/', page_logout, name="logout"),
    path('notes/', NotesView.as_view(), name="notes"),

    path('play/get_characters', get_characters, name="get_characters"),
    path('play/get_map_tile_sets', get_map_tile_sets, name="get_map_tile_sets"),
    path('play/select_character/<str:name>', select_character, name="select_character"),

    path('character_manager/<str:name>/delete/', DeleteCharacterView.as_view(), name="character_delete"),
    # path('character_manager/<str:name>', CharacterManagerView.as_view(), name="character_manager_inside"),
    path('character_manager/', CharactersManagerView.as_view(), name="character_manager"),
    path('character_manager/<str:name>/guild/create/', GuildCreateView.as_view(), name="guild_create"),

    path('characters/<str:name>', view_character),
    path('characters/all/<int:page>', view_all_characters, name="characters_page"),
    path('characters/', RedirectView.as_view(url='/characters/all/1'), name="characters_all"),

    path('guilds/<str:name>', view_guild, name="guild_view"),
    path('guilds/<str:name>/members', view_guild_members, name="guild_members"),
    path('guilds/all/<int:page>', view_all_guilds, name="guild_view_all"),
    path('guilds', RedirectView.as_view(url='/guilds/all/1'), name="all_guild"),
    path('guilds/<str:name>/manage', ManageGuildView.as_view(), name="guild_manage"),
    # path('guilds_manager/<str:name>', view_guild),
]