from django.shortcuts import render, redirect
from characters.models import Character, Account
import json
from django.http import HttpResponse
from django.shortcuts import reverse
from .consumers import ChatConsumer
from .map import worldmap
from redis import Redis

# Just a function, not a view
def fix_game_bugs_after_crash():
    """In case players stayed logged in in after crash - set them logged out."""
    logged_in_chars = Character.objects.filter(logged_in_game=True)
    for char in logged_in_chars:
        char.logged_in_game = False
        char.save()
def game(request):
    """
    Handles request to enter Play page.

    :param request: Django request object.
    :return: (HttpResponse) redirect to homepage or game page.
    """
    try:
        r = Redis('127.0.0.1', socket_connect_timeout=1)
        r.ping()
    except Exception as e:
        ctx = {'server_enabled': False}
        return render(request, "play/play.html", ctx)

    user = request.user
    if user.is_authenticated:
        account = Account.get_from_user(user)
        char_list = Character.objects.filter(user=account.id)
        ctx = {
            'content': 'game',
            'server_enabled': True
        }

        if char_list:
            ctx['characters'] = char_list

        return render(request, "play/play.html", ctx)
    else:
        return redirect(reverse('login'))
def get_characters(request):
    """
    Returns user's list of characters.

    :param request: Django request object.
    :return: (JSON) list of characters.
    """
    if not request.user.is_authenticated:
        return HttpResponse()

    account = Account.get_from_user(request.user)
    characters = Character.objects.filter(user=account.id)
    char_list = list(characters.values_list('name', 'level', 'banned', 'logged_in_game'))

    if len(char_list) == 0:
        return HttpResponse()
    else:
        return HttpResponse(json.dumps(char_list))
def select_character(request, name):
    """
    Make changes in world map, character instance and ChatConsumer object if player allowed to play.
    Informs player if allowed to play.

    :param request: Django request object.
    :param name: Name of selected character
    :return: (JSON) Selected character info or deny info.
    """
    if not request.user.is_authenticated:
        return HttpResponse()

    account = Account.get_from_user(request.user)
    if not account.owns_character(name):
        response = {'accepted': False}
        return HttpResponse(json.dumps(response))

    # check if any character is logged in...
    logged_in_characters = Character.objects.filter(user=account, logged_in_game=True)
    if logged_in_characters:
        response = {
            'accepted': False,
            'error_msg': 'Already logged in.',
        }
        return HttpResponse(json.dumps(response))

    character = account.get_character(name)
    bag = {}

    if character.equipment.bag_0:
        bag['bag_0'] = {}
        bag['bag_0']['game_id'] = character.equipment.bag_0.game_id

    if character.equipment.bag_1:
        bag['bag_1'] = {}
        bag['bag_1']['game_id'] = character.equipment.bag_1.game_id

    content = {
        'name': character.name,
        'banned': character.banned,
        'vocation': character.vocation,
        'level': character.level,
        'experience': character.experience,
        'pos_x': character.pos_x,
        'pos_y': character.pos_y,
        'direction': character.direction,
        'bag': bag,
    }

    response = {
        'accepted': True,
        'content': content,
    }

    worldmap.put_player_into_game_dict(character)
    character.logged_in_game = True
    character.save()
    content['logged_in_game'] = True
    if character not in ChatConsumer.connected_players:
        ChatConsumer.connected_players[character.name] = {
            'character': character,
            'socket': ChatConsumer.all_users[account]['consumer']
        }
    # Lazy way to make it work...
    consumer = ChatConsumer.all_users[account]['consumer']
    consumer.character = character
    character.consumer = consumer

    worldmap.update_vision_map(character)

    return HttpResponse(json.dumps(response))
def get_map_tile_sets(request):
    """
    Return game tile sets info.

    :param request: Django request object.
    :return: (JSON) Tile sets info.
    """
    if not request.user.is_authenticated:
        return HttpResponse()

    response = {
        'tile_set': worldmap.tiles_dict,
    }

    return HttpResponse(json.dumps(response))


# Just in case of crash happening
fix_game_bugs_after_crash()