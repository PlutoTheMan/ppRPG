var test = 0

class Player {
    constructor(data) {
        this.name = data.player_info.name
        this.level = data.player_info.level
        this.experience = data.player_info.experience
        this.vocation = data.player_info.vocation
        this.pos = {
            x: data.player_info.pos_x,
            y: data.player_info.pos_y,
        }
        this.drawPos = screen.getSquareCords(5, 5)

        this.draw_nickname = true
        this.draw_position = true
        this.direction = data.player_info.direction
        // this.speed = 130
        this.speed = 250
        this.speed_reducer = 100 //reduce speed by this amount, letting this.speed to be greater values
        this.offset_bg = 0
        this.interval_background_move = null
        this.animation_step = 0

        this.moving = false

        this.moving_right = false
        this.moving_left = false
        this.moving_top = false
        this.moving_bottom = false

        this.x_modifier1 = 0
        this.x_modifier2 = 0
        this.y_modifier1 = 0
        this.y_modifier2 = 0

        this.interval_move = null
    }

    update_draw_pos(){
        this.drawPos = screen.getSquareCords(5, 5)
    }
    move(direction){
        // This function fires only after server accepts move
        if (this.interval_move != null)
            return false

        this.direction = direction
        this.moving = true

        // // Could set here
        let player_to_move = this

        switch (direction) {
            case 0:
                player_to_move.moving_top = true
                break
            case 1:
                player_to_move.moving_right = true
                break
            case 2:
                player_to_move.moving_bottom = true
                break
            case 3:
                player_to_move.moving_left = true
                break
            }

        switch (direction){
            case 0:
                player_to_move.pos.y -= 1
                break
            case 1:
                player_to_move.pos.x += 1
                break
            case 2:
                player_to_move.pos.y += 1
                break
            case 3:
                player_to_move.pos.x -= 1
                break
        }

        // Setting background offset for correct draw animation
        let context = this
        let timeout_speed = 1000/(this.speed/this.speed_reducer)
        let background_interval = 10
        let times_repeated = timeout_speed / background_interval

        this.interval_move = setInterval(function (){
            worldmap.draw_all_players()
            // worldmap.draw_all_items()
            // console.log(context.offset_bg)
            // !Square width or height doesn't matter as long as they are the same value
            context.offset_bg += square_width*game_view_multiplier/times_repeated*(context.speed/context.speed_reducer)/2
            context.animation_step += 0.15
        }, background_interval * game_view_multiplier/2)
        setTimeout(function(){
            clearInterval(context.interval_move)
            context.interval_move = null
            context.moving = false

            context.offset_bg = 0
            context.animation_step = 0
            context.moving_right = false
            context.moving_left = false
            context.moving_bottom = false
            context.moving_top = false
        }, timeout_speed/(this.speed/context.speed_reducer))
    }
    animate_disconnect(){

    }

    update_relative_draw_data(rel_player){
        if (rel_player.moving_right){
            rel_player.y_modifier1 = 0
            rel_player.y_modifier2 = 0
            rel_player.x_modifier1 = -1
            rel_player.x_modifier2 = square_width
        } else if (rel_player.moving_left){
            rel_player.y_modifier1 = 0
            rel_player.y_modifier2 = 0
            rel_player.x_modifier1 = 1
            rel_player.x_modifier2 = -square_width
        } else if (rel_player.moving_bottom){
            rel_player.x_modifier1 = 0
            rel_player.x_modifier2 = 0
            rel_player.y_modifier1 = -1
            rel_player.y_modifier2 = square_width
         } else if (rel_player.moving_top){
            rel_player.x_modifier1 = 0
            rel_player.x_modifier2 = 0
            rel_player.y_modifier1 = 1
            rel_player.y_modifier2 = -square_width
        }
    }

    draw_relative_to(rel_player){
        let draw_pos = screen.getSquareCords(this.pos.x - rel_player.pos.x + Math.floor(x_squares/2), this.pos.y - rel_player.pos.y + Math.floor(y_squares/2))

        this.update_relative_draw_data(rel_player)
        this.update_relative_draw_data(this)

        // Different calculations needed when net_player is moving, so I use moving_modifier
        let moving_modifier = this.moving ? 1 : 0;

        if (this.direction==1){
            ctx_players.drawImage(
                spr_player,
                Math.floor(this.animation_step)%8 * 64,
                64*8+3*64,
                64,64,
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2),
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2),
                square_width + 1, square_height
            );
        } else if (this.direction==3){
            ctx_players.drawImage(
                spr_player,
                Math.floor(this.animation_step)%8*64,
                64*8+1*64,
                64,64,
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2),
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2),
                square_width + 1, square_height
            );
        } else {
            ctx_players.drawImage(
                spr_player,
                Math.floor(this.animation_step) % 8 * 64, 64 * 8 + this.direction * 64,
                64, 64,
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2),
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                 - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2),
                square_width + 1, square_height
            )


        }

        if (this.draw_nickname){
            ctx_players.fillStyle = 'rgba(255,255,255,0.79)';
            ctx_players.fillRect(
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2)+1-square_width/4,
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                 - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2)-15,
                square_width*1.5, 15)
            ctx_players.textAlign = "center";
            ctx_players.font = "bold 14px serif";
            ctx_players.fillStyle = '#000000';
            ctx_players.fillText(
                this.name,
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2) + square_size_base,
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                 - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2) - 2);

        }

        if (this.draw_position){
            ctx_players.fillStyle = 'rgba(255,255,255,0.79)';
            ctx_players.fillRect(
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2)+1-square_width/4,
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                 - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2) + square_height + 3,
                square_width*1.5, 15)
            ctx_players.fillStyle = '#000000'

            ctx_players.fillText(
                `x: ${this.pos.x}, y: ${this.pos.y}`,
                draw_pos.x1 + rel_player.offset_bg * rel_player.x_modifier1 + rel_player.x_modifier2
                - moving_modifier*(this.offset_bg * this.x_modifier1) - moving_modifier*(this.x_modifier2) + square_size_base,
                draw_pos.y1 + rel_player.offset_bg * rel_player.y_modifier1 + rel_player.y_modifier2
                 - moving_modifier*(this.offset_bg * this.y_modifier1) - moving_modifier*(this.y_modifier2) + square_height + 15
            )

        }

        // Required for correct draw positions after main character stopped moving
        rel_player.x_modifier2 = 0
        rel_player.y_modifier2 = 0
    }


}

class MainPlayer extends Player {
    constructor(data) {
        super(data);
        this.listener = null
        this.init_listener()
        this.moving_left = false
        this.moving_right = false
        this.moving_top = false
        this.moving_bottom = false
        this.inventory = data.inventory
        this.draw()
        this.pressing_move_top = false
        this.pressing_move_right = false
        this.pressing_move_bottom = false
        this.pressing_move_left = false

        this.move_send_delay = 50
        this.move_send_last_send = Date.now() - this.move_send_delay

        this.action_send_delay = 50
        this.action_send_last_send = Date.now() - this.action_send_delay
    }

    init_listener(){
        let context = this
        this.listener = window.addEventListener("keydown", function(e){
            if (game_chat.is_active())
                return false

            switch (e.key) {
                // Movement
                case "w":
                    context.pressing_move_right = false
                    context.pressing_move_bottom = false
                    context.pressing_move_left = false
                    context.pressing_move_top = true
                    break
                case "d":
                    context.pressing_move_bottom = false
                    context.pressing_move_left = false
                    context.pressing_move_top = false
                    context.pressing_move_right = true
                    break
                case "s":
                    context.pressing_move_right = false
                    context.pressing_move_left = false
                    context.pressing_move_top = false
                    context.pressing_move_bottom = true
                    break
                case "a":
                    context.pressing_move_right = false
                    context.pressing_move_bottom = false
                    context.pressing_move_top = false
                    context.pressing_move_left = true
                    break
                // Inventory
                case "i":
                    context.inventory.toggle()
                    break
            }
        })

        window.addEventListener("keyup", function(e){
            switch (e.key) {
                case "w":
                    context.pressing_move_top = false
                    break
                case "d":
                    context.pressing_move_right = false
                    break
                case "s":
                    context.pressing_move_bottom = false
                    break
                case "a":
                    context.pressing_move_left = false
                    break
            }
        })
    }
    update(){
        if (this.moving){
            this.draw()
            worldmap.draw_all_items()
        }

        if (this.pressing_move_top){
            this._move(0)
        }
        if (this.pressing_move_right){
            this._move(1)
        }
        if (this.pressing_move_bottom){
            this._move(2)
        }
        if (this.pressing_move_left){
            this._move(3)
        }
    }
    _move(direction){
        if (!this.moving){
            // Prevent unnecessary too quick request to server
            if (Date.now() - this.move_send_delay > this.move_send_last_send){
                gameSocket.send(JSON.stringify({
                    'move': direction
                }))
                this.move_send_last_send = Date.now()
            }
        }
    }

    move(direction, view){
        // This function fires only after server accepts move
        if (this.interval_background_move != null)
            return false

        this.direction = direction
        this.moving = true

        // Could set here
        let player_to_move = this

        switch (direction) {
            case 0:
                player_to_move.moving_top = true
                break
            case 1:
                player_to_move.moving_right = true
                break
            case 2:
                player_to_move.moving_bottom = true
                break
            case 3:
                player_to_move.moving_left = true
                break
        }

        worldmap.update_items_from_view(JSON.parse(view))
        worldmap.update_all_items()

        switch (direction){
            case 0:
                player_to_move.pos.y -= 1
                break
            case 1:
                player_to_move.pos.x += 1
                break
            case 2:
                player_to_move.pos.y += 1
                break
            case 3:
                player_to_move.pos.x -= 1
                break
        }

        // Moving background for move animation
        let context = this
        let timeout_speed = 1000/(this.speed/this.speed_reducer)
        let background_interval = 10
        let times_repeated = timeout_speed / background_interval
        // console.log(players[0].pos.y)
        this.interval_background_move = setInterval(function (){
            context.animation_step += 0.15
            if (context.direction == 3){
                context.offset_bg += square_width*game_view_multiplier/times_repeated*(context.speed/context.speed_reducer)/2
                canvas_ground.style.left = Math.round(context.offset_bg) -square_width + 'px'
                game_grid.style.left = Math.round(context.offset_bg) -square_width + 'px'
            } else if (context.direction == 1){
                context.offset_bg += square_width*game_view_multiplier/times_repeated*(context.speed/context.speed_reducer)/2
                canvas_ground.style.left = -Math.round(context.offset_bg) -square_width + 'px'
                game_grid.style.left = -Math.round(context.offset_bg) -square_width + 'px'
            } else if (context.direction == 0){
                context.offset_bg += square_width*game_view_multiplier/times_repeated*(context.speed/context.speed_reducer)/2
                canvas_ground.style.top = Math.round(context.offset_bg) -square_height + 'px'
                game_grid.style.top = Math.round(context.offset_bg) -square_height + 'px'
            } else if (context.direction == 2){
                context.offset_bg += square_height*game_view_multiplier/times_repeated*(context.speed/context.speed_reducer)/2
                canvas_ground.style.top = -Math.round(context.offset_bg) -square_height + 'px'
                game_grid.style.top = -Math.round(context.offset_bg) -square_height + 'px'
            }
            // Also draw other players!
            ctx_players.clearRect(0, 0, canvas_players.width, canvas_players.height);
            worldmap.draw_all_players()
        }, background_interval * game_view_multiplier/2)
        setTimeout(function(){
            clearInterval(context.interval_background_move)
            context.interval_background_move = null
            context.moving = false

            context.offset_bg = 0
            canvas_ground.style.left = -square_width + 'px'
            canvas_ground.style.top = -square_height + 'px'
            game_grid.style.left = -square_width + 'px'
            game_grid.style.top = -square_height + 'px'
            context.animation_step = 0
            context.moving_right = false
            context.moving_left = false
            context.moving_bottom = false
            context.moving_top = false
            // worldmap.draw_ground(JSON.parse(view))
            worldmap.draw_ground_layer(JSON.parse(view), 0)
            worldmap.draw_ground_layer(JSON.parse(view), 1)
        }, timeout_speed/(this.speed/context.speed_reducer))
    }
    drag_drop(source_type, destination_type){

        let from_ground_pos = null
        let from_inventory_slot = null
        let to_ground_pos = null
        let to_inventory_slot = null

        if (source_type == "ground"){
            from_ground_pos = ground.dragged_from
            // console.log(`from ${source_type}, pos: ${from_ground_pos.x}, ${from_ground_pos.y}`)
        } else if (source_type == "inventory") {
            from_inventory_slot = main_player.inventory.dragged_from
            // console.log(`from ${source_type} inventory_id: ${from_inventory_slot}`)
        }

        if (destination_type == "ground") {
            to_ground_pos = ground.dragged_to
            // console.log(`to ${destination_type}, pos: ${to_ground_pos.x}, ${to_ground_pos.y}`)
        } else if (destination_type == "inventory") {
            to_inventory_slot = main_player.inventory.drag_destination
            // console.log(`to ${destination_type} inventory_id: ${to_inventory_slot}`)
        }

        let send_type_from = from_ground_pos != null ? "ground" : "inventory"
        let send_type_to = to_ground_pos != null ? "ground" : "inventory"
        let send_from = from_ground_pos != null ? from_ground_pos : from_inventory_slot
        let send_to = to_ground_pos != null ? to_ground_pos : to_inventory_slot
        let data = {
            "source_type": send_type_from,
            "source_value": send_from,
            "target_type": send_type_to,
            "target_value": send_to
        }

        if (Date.now() - this.move_send_delay > this.move_send_last_send){
            // console.log("sending drag action")
            gameSocket.send(JSON.stringify({
                'drag': data
            }))
            this.move_send_last_send = Date.now()
        }

        let context = this
        // console.log(`Dragged from [${from_ground_pos.x}, ${from_ground_pos.y}]
        //  to [${to_ground_pos.x}, ${to_ground_pos.y}]`)
    }

    draw(){
        ctx_players.imageSmoothingEnabled= false

        if (this.direction==1){
            ctx_players.drawImage(spr_player, Math.floor(this.animation_step)%8*64, 64*8+3*64, 64, 64, this.drawPos.x1, this.drawPos.y1, square_width+1, square_height);
        } else if (this.direction==3){
            ctx_players.drawImage(spr_player, Math.floor(this.animation_step)%8*64, 64*8+1*64, 64, 64, this.drawPos.x1, this.drawPos.y1, square_width+1, square_height);
        } else {
            ctx_players.drawImage(spr_player, Math.floor(this.animation_step)%8*64, 64*8+this.direction*64, 64, 64, this.drawPos.x1, this.drawPos.y1, square_width+1, square_height);
        }

        if (this.draw_nickname){
            ctx_players.fillStyle = 'rgba(255,255,255,0.79)';
            ctx_players.fillRect(this.drawPos.x1+1-square_width/4, this.drawPos.y1-15, square_width*1.5, 15)
            ctx_players.textAlign = "center";
            ctx_players.font = "bold 14px serif";
            ctx_players.fillStyle = '#000000';
            ctx_players.fillText(this.name, this.drawPos.x1 + square_size_base, this.drawPos.y1 - 2);
        }

        if (this.draw_position){
            ctx_players.fillStyle = 'rgba(255,255,255,0.79)';
            ctx_players.fillRect(this.drawPos.x1+1-square_width/4, this.drawPos.y1 + square_height + 3, square_width*1.5, 15)
            ctx_players.fillStyle = '#000000';
            ctx_players.fillText(`x: ${this.pos.x}, y: ${this.pos.y}` , this.drawPos.x1 + square_size_base, this.drawPos.y1 + square_height + 15);
        }
    }
}