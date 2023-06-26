class Screen{
    constructor(data) {
        this.update_canvas_styles()
        this.init()
        this._request_view()
    }

    update_canvas_styles(){
        game_width = square_size_base*x_squares*game_view_multiplier
        game_height = square_size_base*y_squares*game_view_multiplier
        screen_width = game_width - square_size_base*2*game_view_multiplier
        screen_height = game_height - square_size_base*2*game_view_multiplier

        content_wrap.style.top = `${square_size_base*game_view_multiplier}px`
        content_wrap.style.width = `${square_size_base*game_view_multiplier*(x_squares-2)}px`
        content_wrap.style.height = `${square_size_base*game_view_multiplier *(y_squares-2)}px`

        canvas_ground.style.left = `${-square_size_base*game_view_multiplier}px`
        canvas_ground.style.top = `${-square_size_base*game_view_multiplier}px`
        canvas_ground.width = `${square_size_base*game_view_multiplier * (x_squares)}`
        canvas_ground.height = `${square_size_base*game_view_multiplier * (y_squares)}`

        game_grid.style.left = `${-square_size_base*game_view_multiplier}px`
        game_grid.style.top = `${-square_size_base*game_view_multiplier}px`
        game_grid.style.width = `${square_size_base*game_view_multiplier * (x_squares)}px`
        game_grid.style.height = `${square_size_base*game_view_multiplier * (y_squares)}`
        game_grid.height = `${square_size_base*game_view_multiplier * (y_squares)}`

        canvas_players.style.left = `${-square_size_base*game_view_multiplier}px`
        canvas_players.style.top = `${-square_size_base*game_view_multiplier}px`
        canvas_players.width = `${square_size_base*game_view_multiplier * (x_squares)}`
        canvas_players.height = `${square_size_base*game_view_multiplier * (y_squares)}`

        canvas_items.style.left = `${-square_size_base*game_view_multiplier}px`
        canvas_items.style.top = `${-square_size_base*game_view_multiplier}px`
        canvas_items.width = `${square_size_base*game_view_multiplier * (x_squares)}`
        canvas_items.height = `${square_size_base*game_view_multiplier * (y_squares)}`

        game_bar.update()

        // square_width = Math.round(canvas.width / x_squares)
        // square_height = Math.round(canvas.height / y_squares)
    }

    init(){
        canvas_ground.style.display = "block"
        canvas_items.style.display = "block"
        canvas_players.style.display = "block"
        game_grid.style.display = "block"
    }
    _request_view(){
        gameSocket.send(JSON.stringify({
            'view': 'get_surrounding'
        }))
    }
    pos_to_tile_cord(pos){
        if (pos.x < main_player.pos.x - 5){
            return false
        }

        if (pos.x > main_player.pos.x + 5){
            return false
        }

        if (pos.y < main_player.pos.y - 5){
            return false
        }

        if (pos.y > main_player.pos.y + 5){
            return false
        }

        let tile_pos = {
            x: Math.abs(main_player.pos.x - pos.x - 5),
            y: Math.abs(main_player.pos.y - pos.y - 5),
        }

        return tile_pos
    }

    pos_to_dictionary_key(pos){
        return 1
    }

    dictionary_key_to_pos(key){
        const pos = key.split(",");
        return {x: pos[0], y: pos[1]}
    }

    getSquareCords(x, y){
        return {
            x1: canvas_ground.width/x_squares * x-1,
            x2: canvas_ground.width/x_squares * (x+1),
            y1: canvas_ground.height/y_squares * y-1,
            y2: canvas_ground.height/y_squares * (y+1),
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

        let draw_pos = null
        if (main_player.moving_bottom){
            draw_pos = this.getSquareCords(tile_pos.x, tile_pos.y + 1)
        } else if (main_player.moving_top) {
            draw_pos = this.getSquareCords(tile_pos.x, tile_pos.y - 1)
        } else if (main_player.moving_left) {
            draw_pos = this.getSquareCords(tile_pos.x - 1, tile_pos.y)
        } else if (main_player.moving_right) {
            draw_pos = this.getSquareCords(tile_pos.x + 1, tile_pos.y)
        } else {
            draw_pos = this.getSquareCords(tile_pos.x, tile_pos.y)
        }

        let img = get_sprite_info(id)

        ctx_ground.imageSmoothingEnabled= false

        // console.log("DRAWING!")
        // console.log(id, img.pos.x, img.pos.y, draw_pos.x1,img.size.width, img.size.height)
        ctx_ground.drawImage(
            img.file,
            img.pos.x,
            img.pos.y,
            img.size.width, img.size.height,
            draw_pos.x1+1,
            draw_pos.y1+1,
            game_view_multiplier*img.size.width,
            game_view_multiplier*img.size.height,
        )

        if (game_settings.draw_ground_id){
            ctx_ground.font = "14px serif";
            ctx_ground.fillStyle = "#0a0909";
            ctx_ground.fillText(`g_id: ${id}`, draw_pos.x1, draw_pos.y1 + 20);
        }
    }
}