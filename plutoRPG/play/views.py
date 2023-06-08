from django.shortcuts import render, redirect
from characters.models import Character, Account
import json
from django.http import HttpResponse
from .consumers import ChatConsumer
from .map import worldmap

def game(request):
    user = request.user
    if user.is_authenticated:
        account = Account.get_from_user(user)
        char_list = Character.objects.filter(user=account.id)
        ctx = {'characters': char_list}
        return render(request, "play/play.html", ctx)
    else:
        return redirect('/login')

def get_characters(request):
    if not request.user.is_authenticated:
        return None

    account = Account.get_from_user(request.user)
    characters = Character.objects.filter(user=account.id)
    # print(characters)
    # values = character.values_list('name', 'level', 'banned')[0]
    char_list = list(characters.values_list('name', 'level', 'banned', 'logged_in_game'))

    return HttpResponse(json.dumps(char_list))

def select_character(request, name):
    if not request.user.is_authenticated:
        return None

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

    # print(bag)
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
        # 'equipment': character.equipment,
        # 'favourites': character.favourites,
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
    consumer = ChatConsumer.all_users[account]['consumer']
    # So you can use character functions from consumers class and consumer function from character class...
    # Probably need to be reorganized
    consumer.character = character
    character.consumer = consumer

    worldmap.update_vision_map(character)

    return HttpResponse(json.dumps(response))

def get_map_tile_sets(request):
    if not request.user.is_authenticated:
        return None

    response = {
        'tile_set': worldmap.tiles_dict,
    }

    return HttpResponse(json.dumps(response))
