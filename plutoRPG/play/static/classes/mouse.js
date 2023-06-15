class Mouse{
    constructor() {
        this.add_event_listeners()
        this.pressed = false

        this.drag_source_type = null
        this.drag_destination_type = null
    }

    add_event_listeners(){
        let context = this
        document.addEventListener("mousedown", function(e){
            context.pressed = true
            if (ground.mouse_on_ground){
                if (main_player.moving_right){
                    ground.dragged_from = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x - 1, y:ground.mouse_on_ground_pos.y})
                } else if (main_player.moving_left){
                    ground.dragged_from = screen.grid_tile_cord_to_real_pos(
                        {x:parseInt(ground.mouse_on_ground_pos.x) + 1, y:ground.mouse_on_ground_pos.y})
                } else if (main_player.moving_bottom) {
                   ground.dragged_from = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x, y:ground.mouse_on_ground_pos.y - 1})
                } else if (main_player.moving_top) {
                   ground.dragged_from = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x, y:parseInt(ground.mouse_on_ground_pos.y) + 1})
                } else {
                    ground.dragged_from = screen.grid_tile_cord_to_real_pos(ground.mouse_on_ground_pos)
                }
                context.drag_source_type = "ground"
                // console.log("START - GROUND" + ground.dragged_from.x + ", " + ground.dragged_from.y)
            } else if (player_inventory.mouse_on_inventory){
                context.drag_source_type = "inventory"
                player_inventory.dragged_from = player_inventory.mouse_on_inventory_id
                // console.log("START - INVENTORY - ID:" + player_inventory.dragged_from)
            }

        })
        document.addEventListener("mouseup", function(e){
            context.pressed = false
            if (ground.mouse_on_ground){
                context.drag_destination_type = "ground"
                if (main_player.moving_right){
                    ground.dragged_to = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x - 1, y:ground.mouse_on_ground_pos.y})
                } else if (main_player.moving_left){
                    ground.dragged_to = screen.grid_tile_cord_to_real_pos(
                        {x:parseInt(ground.mouse_on_ground_pos.x) + 1, y:ground.mouse_on_ground_pos.y})
                } else if (main_player.moving_bottom) {
                   ground.dragged_to = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x, y:ground.mouse_on_ground_pos.y - 1})
                } else if (main_player.moving_top) {
                   ground.dragged_to = screen.grid_tile_cord_to_real_pos(
                        {x:ground.mouse_on_ground_pos.x, y:parseInt(ground.mouse_on_ground_pos.y) + 1})
                } else {
                    ground.dragged_to = screen.grid_tile_cord_to_real_pos(ground.mouse_on_ground_pos)
                }

                main_player.drag_drop(
                    mouse.drag_source_type,
                    mouse.drag_destination_type
                )
            } else if (player_inventory.mouse_on_inventory){
                player_inventory.dragged_to = player_inventory.mouse_on_inventory_id
                context.drag_destination_type = "inventory"
                // console.log("RELEASE - INVENTORY - ID:" + player_inventory.dragged_to)
            }
        })
    }
}