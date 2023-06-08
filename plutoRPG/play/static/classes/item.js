class Item{
    constructor(data) {
        this.server_id = data.server_id
        this.game_id = data.game_id
        this.worldmap = data.worldmap
        this.pos = data.pos
        // console.log("Item instance created")
    }

    update(){
        // console.log(this.pos)
        let x_modifier = 0
        let y_modifier = 0

        if (main_player.moving_right)
            x_modifier = -1
        else if (main_player.moving_left)
            x_modifier = 1
        else if (main_player.moving_top)
            y_modifier = 1
        else if (main_player.moving_bottom)
            y_modifier = -1

        if (Math.abs(this.pos.x - main_player.pos.x + x_modifier) > 4){
            this.remove_from_items_list()
        }
        if (Math.abs(this.pos.y - main_player.pos.y + y_modifier) > 4){
            this.remove_from_items_list()
        }
    }

    remove_from_items_list(){
        delete items[this.game_id]
    }
    draw_relative_to(rel_player){
        let tile_pos = screen.pos_to_tile_cord(this.pos)
        let draw_pos = screen.getSquareCords(tile_pos.x, tile_pos.y)
        let img_data = get_item_sprite_info(this.game_id)
        rel_player.update_relative_draw_data(rel_player)

        ctx_items.drawImage(
            img_data.file,
            img_data.pos.x,
            img_data.pos.y, sprite_size, sprite_size,
            draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2,
            draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2,
            square_width+1, square_height
        )
    }

}