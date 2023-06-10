from django.db import models
from django.contrib.auth.models import User
from play.map import worldmap

# Create your models here.
class Character(models.Model):
    """Representing account's character."""

    CHOICES_VOCATION = (
        (0, 'No Vocation'),
        (1, 'Warrior'),
        (2, 'Mage'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, unique=True)
    banned = models.BooleanField(default=False)
    vocation = models.IntegerField(choices=CHOICES_VOCATION, default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    pos_x = models.IntegerField(default=7)
    pos_y = models.IntegerField(default=9)
    logged_in_game = models.BooleanField(default=False)
    direction = models.IntegerField(default=2)

    async def attempt_item_drag(self, data):
        """
        Checks if drag action made by player is allowed on the server side and may result in item position
        change on game map and sending view to players. Returns None.

        :param data: (dictionary), data send by player, should contain drag source (equipment, ground), drag target and positions.
        :return: Returns None.
        """
        parsed_info = self.drag_get_parsed_pos_if_allowed(data)
        if parsed_info:
            # Need to add item to the map here
            if data['source_type'] == "ground" and data['target_type'] == "ground":
                await worldmap.move_item_from_ground_to_ground(self, data)
            elif data['source_type'] == "inventory" and data['target_type'] == "ground":
                await worldmap.move_item_from_equipment_to_ground(self, data)

    def drag_get_parsed_pos_if_allowed(self, data):
        """
        Validating data sent by player, called from attempt_item_drag method. Return parsed data
        or False.

        :param data: (dictionary), data send by player, should contain drag source (equipment, ground), drag target and positions.
        :return: Return parsed data if validated correctly and drag is allowed or False.
        """
        # Check if user send something stupid
        if 'source_type' not in data:
            return False

        if 'source_value' not in data:
            return False

        if 'target_type' not in data:
            return False

        if 'target_value' not in data:
            return False

        parsed_source_value = None
        parsed_target_value = None

        if data['source_type'] == 'ground':
            if 'x' not in data['source_value']:
                return False
            if 'y' not in data['source_value']:
                return False
            try:
                pos = {
                    'x': int(data['source_value']['x']),
                    'y': int(data['source_value']['y'])
                }
                parsed_source_value = pos
                if abs(self.pos_x - pos['x']) > worldmap.client_width // 2:
                    return False
                if abs(self.pos_y - pos['y']) > worldmap.client_height // 2:
                    return False
            except Exception:
                print("Couldn't parse target_value from ground to int")
                return False
        elif data['source_type'] == 'inventory':
            try:
                parsed_source_value = int(data['source_value'])
                if parsed_source_value > 7 or parsed_source_value < 0:
                    return False
            except Exception:
                print("Couldn't parse source_value from equipment source to int")
                return False

        if data['target_type'] == 'ground':
            if 'x' not in data['target_value']:
                return False
            if 'y' not in data['target_value']:
                return False
            try:
                pos = {
                    'x': int(data['target_value']['x']),
                    'y': int(data['target_value']['y'])
                }
                parsed_target_value = pos
                if abs(self.pos_x - pos['x']) > worldmap.client_width // 2:
                    return False
                if abs(self.pos_y - pos['y']) > worldmap.client_height // 2:
                    return False
            except Exception:
                print("Couldn't parse target_value from ground to int")
                return False
        elif data['target_type'] == 'inventory':
            try:
                parsed_target_value = int(data['target_value'])
                if parsed_target_value > 7 or parsed_target_value < 0:
                    return False
            except Exception:
                print("Couldn't parse target_value from equipment to int")
                return False

        ret = {
            'source_type': data['source_type'],
            'source_value': parsed_source_value,
            'target_type': data['target_type'],
            'target_value': parsed_target_value,
        }
        return ret

    def has_guild(self):
        """
        Checks if player belongs to guild.

        :return: True or False
        """
        if hasattr(self, 'guild'):
            return True
        return False

    def is_guild_leader(self):
        """
        Checks if player is the guild leader.

        :return: True when has guild and is a leader, False if not or doesn't have guild at all.
        """
        if not self.has_guild():
            return False
        if self.guild.leader.pk == self.pk:
            print("is leader of this guild")
            return True
        return False

    def is_logged_in_game(self):
        """
        Checks if player is logged in game.

        :return: Either True or False
        """
        return self.logged_in_game

    def can_chat_globally(self):
        """
        Checks if player meet requirements to use in game global chat.

        :return: True or False if not logged in or doesn't meet requirements.
        """
        if self.is_logged_in_game() and self.level >= 1:
            return True
        return False

    def can_move(self, direction):
        """
        Validates direction data and compare current game state to check if player may move or not.

        :param direction: (number), direction of the movement (top, right, bottom, left).
        :return:
        """
        # Correct direction send check
        if direction not in range(0, 4):
            return False

        x_modifier = -1 if direction == 3 else 1 if direction == 1 else 0
        y_modifier = -1 if direction == 0 else 1 if direction == 2 else 0

        desired_pos = {
            'x': self.pos_x + x_modifier,
            'y': self.pos_y + y_modifier,
        }

        # Map boundary check
        if not (desired_pos['x'] in range(0, worldmap.map_width) and desired_pos['y'] in range(0, worldmap.map_height)):
            return False

        # Player collision check
        tile_parsed = f"{desired_pos['x']},{desired_pos['y']}"
        if 'players' in worldmap.gameMap[tile_parsed]:
            return False


        # Is tile walkable?
        ground_id = worldmap.gameMap[tile_parsed][0]['ground_sprite']
        if 'properties' in worldmap.tiles_dict[ground_id]:
            properties = worldmap.tiles_dict[ground_id]['properties']
            if 'walkable' in properties and not properties['walkable']:
                return False

        # Is tile walkable #2? This is need to check STOP TILES from map editor
        # 2 means third layer on map editor, which is reserved for stop tiles
        if 2 in worldmap.gameMap[tile_parsed]:
            return False

        return True

    def move(self, direction):
        """
        Moves player on game map and send update the player and players around him.

        :param direction: (number), direction of the movement (top, right, bottom, left).
        :return: None
        """
        self.remove_from_map(worldmap)
        if direction == 0:
            self.pos_y -= 1
        elif direction == 1:
            self.pos_x += 1
        elif direction == 2:
            self.pos_y += 1
        elif direction == 3:
            self.pos_x -= 1

        self.direction = direction

        worldmap.put_player_into_game_dict(self)
        worldmap.update_vision_map(self, direction)

    def remove_from_map(self, game_map):
        """
        Remove player from the game map.

        :param game_map: (dictionary) containing the state of game map.
        :return:
        """
        game_map.remove_player_from_map_tile_hes_on(self)

class Skills(models.Model):
    """Representing character's skills."""

    character = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key=True)
    fist = models.CharField(default=1, max_length=4)
    sword = models.CharField(default=1, max_length=4)
    club = models.CharField(default=1, max_length=4)
    axe = models.CharField(default=1, max_length=4)
    shielding = models.CharField(default=1, max_length=4)

class Item(models.Model):
    """Representing the item."""

    # Choices_slot not used yet
    CHOICES_SLOT = (
        (0, 'Left Hand'),
        (1, 'Right Hand'),
        (2, 'Helm'),
        (3, 'Chest'),
        (4, 'Legs'),
        (5, 'Boots'),
        (6, 'Belt'),
        (7, 'Ring'),
        (8, 'Amulet'),
    )

    CHOICES_ITEM = (
        (0, 'Empty_Item'),
        (1, 'Knife'),
        (2, 'Wooden Shield'),
    )

    # game_id of 1 will represent knife
    game_id = models.IntegerField(choices=CHOICES_ITEM, default=0)

class Equipment(models.Model):
    """Representing player's equipment"""
    character = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key=True)
    left_hand = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='left_hand')
    right_hand = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='right_hand')
    legs = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='legs')
    boots = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='boots')
    belt = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='belt')
    ring = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='ring')
    amulet = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='amulet')
    bag_0 = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='bag_0')
    bag_1 = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='bag_1')
    bag_2 = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='bag_2')
    bag_3 = models.OneToOneField(Item, on_delete=models.CASCADE, null=True, related_name='bag_3')

class Account(User):
    """Representing players account"""
    class Meta:
        proxy = True

    @classmethod
    def count_all(cls):
        """
        Counting all accounts created.

        :return: (number) of accounts registered in database.
        """
        return cls.objects.all().count()

    @classmethod
    def get_from_user(cls, user):
        """
        Returns Account instance from django User instance

        :param user: Django user instance.
        :return: Account instance if Django user exists
        """
        try:
            # can `user` be manipulated by web user?
            ret = Account.objects.filter(pk=user.id).first()
            return ret
        except Exception:
            return None

    def owns_character(self, name):
        """
        Checks if account has character with given name.

        :param name: (string), name to be checked.
        :return: True or False
        """
        result = Character.objects.filter(user=self.pk, name=name).first()
        # name may be manipulated
        if result is not None:
            return True
        return False

    def get_character(self, name):
        """
        Returns Character instance if belong to account.

        :param name: (string), name to check.
        :return: Character instance or None.
        """
        result = Character.objects.filter(user=self.pk, name=name).first()
        if result is not None:
            return result
        return None

class Favourites(models.Model):
    """Representing player in game Vip List"""

    # Not implemented yet.
    favourites = models.ManyToManyField(Character)