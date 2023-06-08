class Screen{
    constructor(data) {
        this._request_view()
    }
    _request_view(){
        gameSocket.send(JSON.stringify({
            'view': 'get_surrounding'
        }))
    }
    pos_to_tile_cord(pos){
        let tile_pos = {
            x: Math.abs(main_player.pos.x - pos.x - 5),
            y: Math.abs(main_player.pos.y - pos.y - 5),
        }

        return tile_pos
    }

    getSquareCords(x, y){
        return {
            x1: canvas.width/x_squares * x-1,
            x2: canvas.width/x_squares * (x+1),
            y1: canvas.height/y_squares * y-1,
            y2: canvas.height/y_squares * (y+1),
        }
    }

    grid_tile_cord_to_real_pos(pos){
        return {
            x: main_player.pos.x - (5 - pos.x),
            y: main_player.pos.y - (5 - pos.y),
        }
    }
    draw_item_to_tile(tile_pos, item){
        let draw_pos = this.getSquareCords(tile_pos.x, tile_pos.y)
        let img_data = get_item_sprite_info(item['game_id'])

        ctx_items.imageSmoothingEnabled= false
        ctx_items.drawImage(
            img_data.file, img_data.pos.x, img_data.pos.y, sprite_size, sprite_size,
            draw_pos.x1,
            draw_pos.y1,
            square_width+1, square_height
        )

    }
    draw_to_tile(tile_pos, id){
        // console.log(id)
        if (id === undefined)
            return

        let draw_pos = this.getSquareCords(tile_pos.x, tile_pos.y)
        let img = get_sprite_info(id)
        // console.log(img)
        ctx_ground.imageSmoothingEnabled= false

        ctx_ground.drawImage(
            img.file,
            img.pos.x,
            img.pos.y,
            img.size.width, img.size.height,
            draw_pos.x1,
            draw_pos.y1 + game_view_multiplier*(square_height - img.size.height) - square_height,
            game_view_multiplier*img.size.width+1,
            game_view_multiplier*img.size.height+1,
            // square_width+1, square_height,
            // square_width+1, square_height,
        )

        ctx_ground.font = "14px serif";
        ctx_ground.fillStyle = "#0a0909";
        ctx_ground.fillText(`g_id: ${id}`, draw_pos.x1, draw_pos.y1 + 20);
    }
}