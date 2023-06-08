import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from characters.models import Account, Character
from .map import worldmap

class ChatConsumer(AsyncWebsocketConsumer):
    all_users = {}
    connected_players = {}
    async def connect(self):
        user_id = self.scope["user"].id
        self.account = await get_account(user_id)
        ChatConsumer.all_users[self.channel_name] = {}
        ChatConsumer.all_users[self.channel_name]['account'] = self.account
        ChatConsumer.all_users[self.account] = {}
        ChatConsumer.all_users[self.account]['channel'] = self.channel_name
        ChatConsumer.all_users[self.account]['consumer'] = self

        self.room_group_name = 'group_global'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        try:
            print("consumers..")
            print(self.character.name)
            print(self.character.equipment.bag_0)
        except Exception as e:
            print(e)

        try:
            worldmap.remove_player_from_map_vision_map(self.character)
        except Exception as e:
            print("Couldn't remove vision map on logout")
        try:
            del self.connected_players[self.character.name]
        except Exception:
            print("Failed deleting key from ChatConsumer instance (self.connected_players[self.character.name]")

        try:
            self.character.remove_from_map(worldmap)
        except Exception:
            print("Failed removing Player from map")

        try:
            self.character.logged_in_game = False
            await save_character(self.character)
        except Exception:
            print("Skipping setting to offline, since character not logged in.")

        try:
            msg = f'{self.character.name} has left the game.'
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "request_chat_global", "message": msg, "context": "disconnect",
                "disconnected_player": self.character.name})
        except Exception:
            print("Skipping sending disconnect msg - error occured.")


        ChatConsumer.all_users.pop(self.channel_name, None)
        ChatConsumer.all_users.pop(self.account, None)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # print("TESTING AFTER DISCONNECT:")
        # print(ChatConsumer.all_users)

    async def send_connection_message(self):
        print("!")
        try:
            msg = f'{self.character.name} has joined.'
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "request_chat_global", "message": msg, "context": "connect"})
        except Exception:
            print("Skipping sending disconnect msg - error occured.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "message" in text_data_json:
            message = str(text_data_json["message"])
            if len(message) == 0 or len(message) > 100:
                return False
            if self.character.can_chat_globaly():
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "request_chat_global", "message": message, "author": self.character.name
                })
        elif "move" in text_data_json:
            if self.character.can_move(text_data_json["move"]):
                self.character.move(text_data_json["move"])
                pos_owner = f'{str(self.character.pos_x)},{str(self.character.pos_y)}'

                # Get players that should be updated
                players_list_to_get_view = worldmap.vision_map[pos_owner]
                for player in players_list_to_get_view:
                    if worldmap.vision_map:
                        pos_x = ChatConsumer.connected_players[player]['character'].pos_x
                        pos_y = ChatConsumer.connected_players[player]['character'].pos_y
                        pos = f'{str(pos_x)},{str(pos_y)}'
                        client_view = worldmap.get_character_view(pos)
                        if self.character.name == ChatConsumer.connected_players[player]['character'].name:
                            # Send just for owner
                            await self.send(text_data=json.dumps({
                                'type': 'move',
                                'message': text_data_json["move"],
                                'view': client_view
                            }))
                        else:
                            # Send for anybody else
                            await ChatConsumer.connected_players[player]['socket'].send(text_data=json.dumps({
                                'type': 'view_player_movement',
                                'message': text_data_json["move"],
                                'view': client_view
                            }))
        elif "view" in text_data_json:
            pos = f'{str(self.character.pos_x)},{str(self.character.pos_y)}'
            await self.send(text_data=json.dumps({
                "type": "view",
                "view": worldmap.get_character_view(pos)
            }))
        elif "drag" in text_data_json:
            await self.character.attempt_item_drag(text_data_json['drag'])
            # print(text_data_json)

    async def request_self_view(self):
        print(f'{self.character.name} requested view')
        pos_x = self.character.pos_x
        pos_y = self.character.pos_y
        pos = f'{str(pos_x)},{str(pos_y)}'
        client_view = worldmap.get_character_view(pos)

        await self.send(text_data=json.dumps({
            'type': 'view',
            # 'message': text_data_json["move"],
            'view': client_view
        }))

    async def send_view_to_players(self, pos):
        players_list_to_get_view = worldmap.vision_map[pos]
        for player in players_list_to_get_view:
            if worldmap.vision_map:
                pos_x = ChatConsumer.connected_players[player]['character'].pos_x
                pos_y = ChatConsumer.connected_players[player]['character'].pos_y
                pos = f'{str(pos_x)},{str(pos_y)}'
                client_view = worldmap.get_character_view(pos)
                await ChatConsumer.connected_players[player]['socket'].send(text_data=json.dumps({
                    'type': 'view',
                    'view': client_view,
                }))

    async def request_chat_global(self, event):
        author = "Server"
        msg_context = ""

        ret = {
            'type': 'chat',
        }

        if 'message' in event:
            ret['message'] = event['message']
        if 'author' in event:
            ret['author'] = event['author']
        if 'context' in event:
            ret['msg_context'] = event['context']
        if 'disconnected_player' in event:
            ret['disconnected_player'] = event['disconnected_player']

        await self.send(text_data=json.dumps(ret))

@database_sync_to_async
def get_account(user_id):
    return Account.objects.filter(id=user_id).first()

@database_sync_to_async
def save_character(character):
    character.save()
    character.equipment.save()