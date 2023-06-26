class Ground{
    constructor() {
        this.game_grid = document.getElementById("game_grid")
        this.make_grid_divs_and_set_dataset()
        this.on_mouseenter_events()
        this.on_mouseout_events()

        this.dragged_from = {x:0, y:0}
        this.dragged_to = {x:0, y:0}

        this.mouse_on_ground = false
        this.mouse_on_ground_pos = {
            'x': null,
            'y': null,
        }
        this.tiles_to_animate = {}

        this.currentDate = new Date()
        this.fps_start = this.currentDate.getTime()
        this.fps = 0
        this.elapsed = 0
        this.fps_done = true
        this.fps_interval = 300

        this.animation_step = 0
    }

    calculate_fps(){
        this.fps += 1
        this.elapsed = new Date().getTime() - this.fps_start

        const count = Math.min(1 * this.elapsed, this.fps_interval);

        if (count == this.fps_interval){
            // console.log(this.elapsed)
            this.fps_start = new Date().getTime()
            this.animation_step += 1
            ground.draw_animated_tiles()
        }
    }

    draw_animated_tiles(){
        for (let tile in this.tiles_to_animate){
            let id = this.tiles_to_animate[tile]
            let pos = screen.pos_to_tile_cord(screen.dictionary_key_to_pos(tile))
            if (pos){
                let piece = this.animation_step % (get_sprite_info(id)['animate_length'])
                // console.log(id + piece)
                screen.draw_to_tile(pos, id + piece, main_player)
            } else {
                delete this.tiles_to_animate[tile]
            }
        }
    }
    update_animations(){
        for (let tile in this.tiles_to_animate){
            if (screen.pos_to_tile_cord(screen.dictionary_key_to_pos(tile))){
                // this.draw_animated_tile()
            } else {
                delete this.tiles_to_animate[tile]
            }
        }
    }

    // draw_animated_tiles(){
    //     for (let tile in this.tiles_to_animate){
    //         if (screen.pos_to_tile_cord(screen.dictionary_key_to_pos(tile))){
    //             this.draw_animated_tile()
    //         } else {
    //             delete this.tiles_to_animate[tile]
    //         }
    //     }
    // }
    make_grid_divs_and_set_dataset(){
        for (let y=1; y <= y_squares; y++){
            for (let x=1; x <= x_squares; x++){
                const div = document.createElement("div")

                div.classList.add('border-inner-grid', 'inline-block', 'm-0', 'p-0')
                div.dataset.x = (x-1).toString()
                div.dataset.y = (y-1).toString()
                div.style.width = `${square_width}px`
                div.style.height = `${square_height}px`

                game_grid.append(div)
                if (x==x_squares){
                    div.classList.add('border-last-right')
                }

                if (y==y_squares){
                    div.classList.add('border-last-bottom')
                }
            }
        }
    }

    update_grid_divs(){
        for (let y=0; y < y_squares; y++){
            for (let x=0; x < x_squares; x++){
                const div = document.querySelector(`[data-x="${x}"][data-y="${y}"]`)
                div.style.width = `${square_width}px`
                div.style.height = `${square_height}px`
            }
        }
    }

    grid_remove_mesh(){
        for (let y=0; y < y_squares; y++){
            for (let x=0; x < x_squares; x++){
                const div = document.querySelector(`[data-x="${x}"][data-y="${y}"]`)
                div.classList.remove('border-inner-grid', 'm-0', 'p-0', 'border-last-right', 'border-last-bottom')

                if (x==x_squares){
                    div.classList.add('border-last-right')
                }

                if (y==y_squares){
                    div.classList.add('border-last-bottom')
                }
            }
        }
    }
    grid_add_mesh(){
        for (let y=0; y < y_squares; y++){
            for (let x=0; x < x_squares; x++){
                const div = document.querySelector(`[data-x="${x}"][data-y="${y}"]`)
                div.classList.add('border-inner-grid', 'm-0', 'p-0')
            }
        }
    }
    on_mouseenter_events(){
        let context = this
        for (let y=1; y <= y_squares; y++){
            for (let x=1; x <= x_squares; x++) {
                let x_val = (x-1).toString()
                let y_val = (y-1).toString()
                let div = document.querySelector(`[data-x="${x_val}"][data-y="${y_val}"]`)
                div.addEventListener('mouseenter', function(e){
                    e.target.classList.add("ground_highlight")
                    if (mouse.pressed){
                        e.target.classList.add("ground_highlight_drag")
                    }

                    context.mouse_on_ground_pos.x = e.target.dataset.x
                    context.mouse_on_ground_pos.y = e.target.dataset.y

                    context.mouse_on_ground = true
                    player_inventory.mouse_on_inventory = false
                })
            }
        }
    }
    on_mouseout_events(){
        let context = this
        for (let y=1; y <= y_squares; y++){
            for (let x=1; x <= x_squares; x++) {
                let x_val = (x-1).toString()
                let y_val = (y-1).toString()
                let div = document.querySelector(`[data-x="${x_val}"][data-y="${y_val}"]`)
                div.addEventListener('mouseout', function(e){
                    e.target.classList.remove("ground_highlight")
                    if (e.target.classList.contains("ground_highlight_drag")){
                        e.target.classList.remove("ground_highlight_drag")
                    }
                    context.mouse_on_ground = false
                })
            }
        }
    }

}