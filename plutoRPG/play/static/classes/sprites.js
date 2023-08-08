const sprite_size = 32

const spr_ground_1 = new Image()
spr_ground_1.src = "/static/sprites/1.png"

const ghost_image = new Image()
ghost_image.src = "/static/sprites/ghost_image.png"

const spr_ground_2 = new Image()
spr_ground_2.src = "/static/sprites/2.png"

const spr_ground_3 = new Image()
spr_ground_3.src = "/static/sprites/shallow_water.png"

const spr_ground_4 = new Image()
spr_ground_4.src = "/static/sprites/lava.png"

const spr_movement_block = new Image()
spr_movement_block.src = "/static/sprites/movement_block.png"

const spr_house_floor_misc = new Image()
spr_house_floor_misc.src = "/static/sprites/house_floor_misc.png"

const spr_house_walls = new Image()
spr_house_walls.src = "/static/sprites/house_walls.png"

const spr_player = new Image()
spr_player.src = "/static/sprites/character.png"

const spr_weapons_1 = new Image()
spr_weapons_1.src = "/static/sprites/weapons.png"

file_source_images = {
    'sprites/shallow_water.png': spr_ground_3,
    'sprites/lava.png': spr_ground_4,
    'sprites/1.png': spr_ground_1,
    'sprites/2.png': spr_ground_2,
    'sprites/weapons.png': spr_weapons_1,
    'sprites/house_floor_misc.png': spr_house_floor_misc,
    'sprites/house_walls.png': spr_house_walls,
    'sprites/movement_block.png': spr_movement_block,
}

let sprite_list = null
function get_sprite_info(id){
    let ret = {
        'file': file_source_images[sprite_list['tile_set'][id]['file']],
        'pos': {
            'x': sprite_list['tile_set'][id]['pos']['x'],
            'y': sprite_list['tile_set'][id]['pos']['y']
        },
        'size': {
            'width': sprite_list['tile_set'][id]['size']['width'],
            'height': sprite_list['tile_set'][id]['size']['height'],
        }
    }

    if ('properties' in sprite_list['tile_set'][id]){
        for (let property in sprite_list['tile_set'][id]['properties']){
            ret[property] = sprite_list['tile_set'][id]['properties'][property]
        }
    }
    return ret
}

const weapons_sprite_list = {
    1: {
        file: file_source_images['sprites/weapons.png'],
        pos:{
            'x': 0,
            'y': 0,
        }
    }
}
function get_item_sprite_info(game_id){
    return {
        'file': weapons_sprite_list[game_id]['file'],
        'pos': weapons_sprite_list[game_id]['pos']
    }
}

