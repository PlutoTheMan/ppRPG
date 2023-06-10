import pytest
from play import map

@pytest.mark.django_db
def test_correct_keys_based_on_map_size():
    worldmap = map.WorldMap()
    worldmap.gameMap = {}
    worldmap.parse_layers_for_game_dict()

    check_keys_existent = True
    for count, key in enumerate(worldmap.gameMap):
        if key != f'{count % worldmap.map_width},{count // worldmap.map_width}':
            check_keys_existent = False
            break

    assert check_keys_existent

def test_no_empty_tiles_on_ground_level():
    worldmap = map.WorldMap()
    check_level_0_key = True
    check_ground_sprite_key = True
    for key in worldmap.gameMap:
        if 0 not in worldmap.gameMap[key]:
            check_level_0_key = False
            break

        if 'ground_sprite' not in worldmap.gameMap[key][0]:
            check_ground_sprite_key = False

    assert check_level_0_key and check_ground_sprite_key
