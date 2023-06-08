class Worldmap {
    constructor() {
        this.screen = ""
        this.last_view = null
        this.last_player_view = null
    }

    disconnect_player(player_name){
        let worldmap = this
        players.forEach(function(player, i){
            if (player.name == player_name){
                players[i].animate_disconnect()
                players.splice(i, 1)
                worldmap.delete_player_from_last_player_view(player_name)
                console.log("disconnecting:" + player_name)
                worldmap.draw_from_view_player_movement(worldmap.last_player_view)
            }
        })

    }

    draw_all_players(){
        ctx_players.clearRect(0, 0, canvas_players.width, canvas_players.height)
        players.forEach(function(player){
            player.draw_relative_to(main_player)
        })
        main_player.draw()
    }

    update_all_items(){
        for (let item in items){
            items[item].update()
        }
    }
    draw_all_items(){
        ctx_items.clearRect(0, 0, canvas_items.width, canvas_items.height)
        for (let item in items){
            items[item].draw_relative_to(main_player)
        }
        main_player.draw()
    }

    delete_player_from_last_player_view(name){
        let worldmap = this

        for (let k in worldmap.last_player_view){
            let pos = k.split(",")
            let layers = worldmap.last_player_view[k]

            for (let layer in layers){
                switch (layer){
                    case 'players':
                        let players_on_screen = layers[layer]

                        for (let player in players_on_screen) {
                            let p = players_on_screen[player]
                            if (p.name == name){
                                console.log(`deleting ${name}`)
                                delete players_on_screen[player]
                                if (Object.keys(players_on_screen).length == 0){
                                    delete layers.players
                                }
                                break
                            }
                        }

                        worldmap.draw_all_players()

                        break
                }
            }
        }

    }

    async draw_from_view_player_movement(view){
        // Delete players from list that are not on the list
        players.forEach(function(player, i){
            if (Math.abs(player.pos.x - main_player.pos.x) >= 6){
                players.splice(i, 1)
            }
        })

        for (let k in view){
            let pos = k.split(",")
            let real_pos = {'x': Number(pos[0]), y:Number(pos[1])}
            let layers = view[k]

            for (let layer in layers){
                switch (layer){
                    case 'players':
                        let tile_pos = this.screen.pos_to_tile_cord(real_pos)
                        let players_on_screen = layers[layer]


                        for (let player in players_on_screen) {
                            let p = players_on_screen[player]

                            if (p.name == main_player.name){
                                break
                            }

                            let found = false

                            for (let i = 0; i < players.length; i++){
                                if (players[i].name == player){
                                    players[i].move(players_on_screen[player].direction)
                                    found = true
                                    break
                                }
                            }

                            if (!found){
                                console.log("NOT FOUND")
                                let p = players_on_screen[player]
                                let player_data = {
                                    'worldmap': worldmap,
                                    'player_info': {
                                        'name': p.name,
                                        'level': p.level,
                                        'pos_x': real_pos.x,
                                        'pos_y': real_pos.y,
                                        'direction': p.direction,
                                    }
                                }

                                const new_player = new Player(player_data)
                                players.push(new_player)
                                new_player.draw_relative_to(main_player)
                            }
                        }

                        break
                }
            }

        }
        this.last_player_view = view
    }

    draw_ground(data){
        ctx_ground.clearRect(0, 0, canvas_ground.width, canvas_ground.height);

        for (let k in data){

            let pos = k.split(",")
            let real_pos = {'x': Number(pos[0]), y:Number(pos[1])}
            let layers = data[k]

            for (let layer in layers){
                switch (layer){
                    case 'players':
                        continue
                }

                // IF GROUND
                let tile_pos = this.screen.pos_to_tile_cord(real_pos)
                let id = layers[layer]["ground_sprite"]
                this.screen.draw_to_tile(tile_pos, id, main_player)
            }
        }

        this.last_view = data
    }

    draw_ground_and_player(data){
        // Delete players from list that are not on the list
        players.forEach(function(player, i){
            if (Math.abs(player.pos.x - main_player.pos.x) >= 6){
                players.splice(i, 1)
            }
        })

        main_player.draw()

        ctx_ground.clearRect(0, 0, canvas_ground.width, canvas_ground.height);

        for (let k in data){
            let pos = k.split(",")
            let real_pos = {'x': Number(pos[0]), y:Number(pos[1])}
            let layers = data[k]
            let tile_pos

            for (let layer in layers){
                switch (layer){
                    case 'players':
                        tile_pos = this.screen.pos_to_tile_cord(real_pos)
                        let players_on_screen = layers[layer]

                        for (let player in players_on_screen) {
                            let p = players_on_screen[player]

                            if (p.name == main_player.name){
                                break
                            }

                            let found = false
                            for (let i = 0; i < players.length; i++){
                                if (players[i].name == player){
                                    players[i].pos.x = real_pos.x
                                    players[i].pos.y = real_pos.y
                                    players[i].direction = players_on_screen[player].direction
                                    // Set is moving to true
                                    found = true
                                    break
                                }
                            }

                            if (!found){
                                let p = players_on_screen[player]
                                let data = {
                                    'worldmap': worldmap,
                                    'player_info': {
                                        'name': p.name,
                                        'level': p.level,
                                        'pos_x': real_pos.x,
                                        'pos_y': real_pos.y,
                                        'direction': p.direction,
                                    }
                                }

                                const new_player = new Player(data)
                                players.push(new_player)
                                new_player.draw_relative_to(main_player)
                            }
                        }
                        break

                    case "items":
                        ctx_items.clearRect(0, 0, canvas_items.width, canvas_items.height)
                        for (let item in layers.items){
                            let tile_pos = this.screen.pos_to_tile_cord(real_pos)
                            // Draw item...
                            this.screen.draw_item_to_tile(tile_pos, layers.items[item])
                        }

                        let items_on_screen = layers[layer]
                        console.log(items_on_screen)
                        for (let item in items_on_screen) {
                            let it = items_on_screen[item]
                            console.log(it)

                            let found = false
                            // Update item pos if item already registered in items list

                            console.log(items)
                            if (it.id in items){
                                console.log("Updating item")
                                items[it.id].pos.x = real_pos.x
                                items[it.id].pos.y = real_pos.y
                                found = true
                                break
                            }

                            // Append item to the items list if not added yet
                            if (!found){
                                let data = {
                                    'server_id': it.id,
                                    'game_id': it.game_id,
                                    'worldmap': worldmap,
                                    'pos': {
                                        'x': real_pos.x,
                                        'y': real_pos.y,
                                    }
                                }

                                const new_item = new Item(data)
                                items[it.id] = new_item
                                new_item.draw_relative_to(main_player)
                            }
                        }
                        break

                    case "0":
                        // console.log(this)
                        tile_pos = this.screen.pos_to_tile_cord(real_pos)
                        let id = layers[layer]["ground_sprite"]
                        this.screen.draw_to_tile(tile_pos, id, main_player)
                        break
                }
            }
        }

        this.last_view = data
    }

    draw_ground_layer(data, layer_number){
        for (let k in data){
            let pos = k.split(",")
            let real_pos = {'x': Number(pos[0]), y:Number(pos[1])}
            let layers = data[k]
            let tile_pos

            for (let layer in layers){
                switch (layer){
                    case layer_number.toString():
                        tile_pos = this.screen.pos_to_tile_cord(real_pos)
                        let id = layers[layer]["ground_sprite"]
                        this.screen.draw_to_tile(tile_pos, id, main_player)
                        break
                }
            }
        }
    }
    update_items_from_view(data){
        for (let k in data){
            let pos = k.split(",")
            let real_pos = {'x': Number(pos[0]), y:Number(pos[1])}
            let layers = data[k]
            for (let layer in layers){
                switch (layer){
                    case "items":
                        for (let item in layers.items){
                            let tile_pos = this.screen.pos_to_tile_cord(real_pos)
                            // Draw item...
                            this.screen.draw_item_to_tile(tile_pos, layers.items[item])
                        }

                        let items_on_screen = layers[layer]
                        for (let item in items_on_screen) {
                            let it = items_on_screen[item]

                            let found = false
                            // Update item pos if item already registered in items list
                            if (it.id in items){
                                items[it.id].pos.x = real_pos.x
                                items[it.id].pos.y = real_pos.y
                                found = true
                                break
                            }

                            // Append item to the items list if not added yet
                            if (!found){
                                let data = {
                                    'server_id': it.id,
                                    'game_id': it.game_id,
                                    'worldmap': worldmap,
                                    'pos': {
                                        'x': real_pos.x,
                                        'y': real_pos.y,
                                    }
                                }

                                const new_item = new Item(data)
                                items[it.id] = new_item
                                new_item.draw_relative_to(main_player)
                            }
                        }
                }

                // IF GROUND
                // let tile_pos = this.screen.pos_to_tile_cord(real_pos)
                // let id = layers[layer]["ground_sprite"]
                // this.screen.draw_to_tile(tile_pos, id, main_player)
            }


        }

        this.last_view = data
    }
}