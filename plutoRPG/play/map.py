import json
import math

class WorldMap:
    """Representing game map and game state"""
    def __init__(self):
        json_items = open('items/items.json')
        self.items = {}
        self.raw_items = json.load(json_items)
        self.parse_items()
        json_items.close()

        json_data = open('play/static/worldmap.json')
        self.raw_map = json.load(json_data)
        json_data.close()

        self.layers = self.raw_map['layers']
        self.gameMap = {}
        self.vision_map = {}

        self.parse_layers_for_game_dict()
        self.client_width = 9
        self.client_height = 9

        self.map_width = 50
        self.map_height = 50

        self.tiles_dict = {}
        self.parse_sprites()

    async def move_item_from_ground_to_ground(self, character, data):
        """
        Attempt moving item from pos A to pos B on the map by player after data validation

        :param character: Character instance
        :param data: Drag data
        :return: True if drag completed successfully, False if not
        """
        pos_from = f"{data['source_value']['x']},{data['source_value']['y']}"
        pos_to = f"{data['target_value']['x']},{data['target_value']['y']}"

        if 'items' not in self.gameMap[pos_from]:
            return False

        try:
            items = self.gameMap[pos_from]['items']
            # Remove from source...
            last_item_id = list(items.keys())[-1]
            moved_item_info = self.gameMap[pos_from]['items'][last_item_id]
            del self.gameMap[pos_from]['items'][last_item_id]
            if not self.gameMap[pos_from]['items']:
                del self.gameMap[pos_from]['items']
            # Add to destination...
            if 'items' not in self.gameMap[pos_to]:
                self.gameMap[pos_to]['items'] = {}
            self.gameMap[pos_to]['items'][last_item_id] = moved_item_info
        except Exception as e:
            print(e)
            return False

        # await character.consumer.send_items_view_to_players(pos_to)
        await character.consumer.send_view_to_players(pos_to)

    async def move_item_from_equipment_to_ground(self, character, data):
        """
        Attempt moving item from inventory position to ground position on the map by player after data validation

        :param character: Character instance
        :param data: Drag data
        :return: True if drag completed successfully, False if not
        """
        from_eq_pos = data['source_value']
        pos_to = f"{data['target_value']['x']},{data['target_value']['y']}"
        parsed_key = f"bag_{from_eq_pos}"

        try:
            item = getattr(character.equipment, parsed_key)
        except Exception:
            print("Couldn't get item from player equipment")
            return False

        try:
            # Put item on the ground...
            if 'items' not in self.gameMap[pos_to]:
                self.gameMap[pos_to]['items'] = {}
            self.gameMap[pos_to]['items'][item.pk] = {"id": item.pk, "game_id": item.game_id}
            # Removes item from backpack...
            setattr(character.equipment, parsed_key, None)
            await character.consumer.send_view_to_players(pos_to)
        except Exception as e:
            print(e)
            return False

    def parse_items(self):
        """
        Parsing items from JSON file
        :return: None
        """
        for item in self.raw_items:
            self.items[item] = self.raw_items[item]

    def parse_sprites(self):
        """
        Parsing items from JSON file
        :return: None
        """
        for tile_set in self.raw_map['tilesets']:
            tile_set_data = open(f"play/static/{tile_set['source']}")
            tile_data = json.load(tile_set_data)

            for n in range(0, tile_data['tilecount']):
                tile_id = tile_set['firstgid'] + n
                self.tiles_dict[tile_id] = {
                    'file': tile_data['image'],
                    'pos': {
                        'x': tile_data['tilewidth']*n % tile_data['imagewidth'],
                        'y': math.floor(n / tile_data['columns'])*tile_data['tileheight']

                    },
                    'size': {
                        'width': tile_data['tilewidth'],
                        'height': tile_data['tileheight'],
                    }
                }
                if 'tiles' in tile_data:
                    if tile_data['tiles'][0]['id'] == tile_id-1:
                        self.tiles_dict[tile_id]['properties'] = {}
                        properties = tile_data['tiles'][0]['properties']
                        for prop in properties:
                            self.tiles_dict[tile_id]['properties'][prop['name']] = prop['value']

            tile_set_data.close()

    def get_layers_data(self):
        """
        Made for easier readability
        :return:
        """
        ret = {}
        for layer in self.layers:
            ret[layer['name']] = layer['data']

        return ret

    def put_player_into_game_dict(self, character):
        """
        Puts player info on game map
        :param character: Character instance
        :return:
        """
        if character.pos_x not in range(0, self.map_width):
            return False

        if character.pos_y not in range(0, self.map_height):
            return False

        t = f"{character.pos_x},{character.pos_y}"

        if 'players' not in self.gameMap[t]:
            self.gameMap[t]['players'] = {}

        self.gameMap[t]['players'][character.name] = {
            'name': character.name,
            'level': character.level,
            'direction': character.direction,
        }

    def is_inside_map(self, x=0, y=0):
        """
        Checks if position is inside map boundaries.
        :param x: (int), x_position
        :param y: (int), y_position
        :return: True or False
        """
        if x not in range(0, self.map_width):
            return False

        if y not in range(0, self.map_width):
            return False

        return True

    def remove_player_from_map_vision_map(self, character):
        """
        Removes player from vision map
        :param character: Character instance
        :return: None
        """

        first_x = character.pos_x - self.client_width // 2
        first_y = character.pos_y - self.client_height // 2

        for x in range(first_x-1, first_x+self.client_width):
            for y in range(first_y-1, first_y+self.client_height):
                if self.is_inside_map(x=x, y=y):
                    # for now, just update every tile...
                    # performance tip: update based on direction
                    t = f"{x},{y}"
                    if t in self.vision_map:
                        if character.name in self.vision_map[t]:
                            self.vision_map[t].remove(character.name)
                    else:
                        continue

                    if not self.vision_map[t]:
                        del self.vision_map[t]


    def update_vision_map(self, character, direction=5):
        """
        Changes vision map based on player movement

        :param character: Character instance
        :param direction: Direction player is moving
        :return: None
        """
        # 5 means out of 4 directions as default
        def update_vision_map_horizontal(pos_y):
            """
            Changes vision map based on player movement (#redundant #notime)
            :param pos_y: (int) Y position
            :return: None
            """
            for pos_x in range(first_x, first_x + self.client_width):
                if self.is_inside_map(x=pos_x, y=pos_y):
                    key_position = f"{pos_x},{pos_y}"
                    try:
                        self.vision_map[key_position].remove(character.name)
                        if not self.vision_map[key_position]:
                            del self.vision_map[key_position]
                    except Exception:
                        pass

        def update_vision_map_vertical(pos_x):
            """
            Changes vision map based on player movement (#redundant #notime)
            :param pos_x: (int) X position
            :return: None
            """
            for pos_y in range(first_y, first_y + self.client_height):
                if self.is_inside_map(x=pos_x, y=pos_y):
                    key_position = f"{pos_x},{pos_y}"
                    try:
                        self.vision_map[key_position].remove(character.name)
                        if not self.vision_map[key_position]:
                            del self.vision_map[key_position]
                    except Exception:
                        pass

        first_x = character.pos_x - self.client_width//2
        first_y = character.pos_y - self.client_height//2

        for x in range(first_x, first_x+self.client_width):
            for y in range(first_y, first_y+self.client_height):
                if self.is_inside_map(x=x, y=y):
                    # for now, just update every tile...
                    # performance tip: update based on direction
                    t = f"{x},{y}"
                    if t in self.vision_map:
                        if character.name not in self.vision_map[t]:
                            self.vision_map[t].append(character.name)
                    else:
                        self.vision_map[t] = [character.name]

        # now delete these based on direction...
        if direction == 0:
            update_vision_map_horizontal(first_y + self.client_height)
        elif direction == 1:
            update_vision_map_vertical(first_x - 1)
        elif direction == 2:
            update_vision_map_horizontal(first_y - 1)
        elif direction == 3:
            update_vision_map_vertical(first_x + self.client_width)
        elif direction == 5:
            pass

    def remove_player_from_map_tile_hes_on(self, character):
        """
        Removes player from game map on his actual position

        :param character: Character instance
        :return: None
        """
        tile = f"{character.pos_x},{character.pos_y}"
        del self.gameMap[tile]['players'][character.name]

        if not self.gameMap[tile]['players']:
            del self.gameMap[tile]['players']

    def parse_layers_for_game_dict(self):
        """Parsing data for game map"""
        layer_data = self.get_layers_data()
        for layer_index, key in enumerate(layer_data):
            width = self.layers[layer_index]['width']
            height = self.layers[layer_index]['height']
            # slicing map to get x, y tuples for game map
            for y in range(0, height):
                row_start = y * width
                row = layer_data[key][row_start:row_start+width]
                pos_y = y
                for x, value in enumerate(row):
                    if value != 0:
                        # key as str, for easier json.dumps
                        t = f"{x},{y}"
                        if t not in self.gameMap:
                            self.gameMap[t] = {}

                        if layer_index not in self.gameMap:
                            self.gameMap[t][layer_index] = {}

                        self.gameMap[t][layer_index] = {'ground_sprite': value}

    def get_character_view(self, pos):
        """
        Gets character 9x9 (or 1 unit more for client correct display) view as JSON
        :param pos: center position
        :return: view as JSON
        """
        pos_x = 0
        pos_y = 0

        # parse pos argument
        try:
            sent_pos = pos.split(",")
            pos_x = int(sent_pos[0])
            pos_y = int(sent_pos[1])
        except Exception:
            return None

        ret = {}

        # Range is +1 extra from all the sides
        for x in range(pos_x - (self.client_width-1)//2 - 1, pos_x + (self.client_width+1)//2 + 1):
            for y in range(pos_y - (self.client_height-1)//2 - 1, pos_y + (self.client_height+1)//2 + 1):
                key = f'{str(x)},{str(y)}'
                if key in self.gameMap:
                    ret[key] = self.gameMap[key]

        if not ret:
            return None
        return json.dumps(ret)


worldmap = WorldMap()