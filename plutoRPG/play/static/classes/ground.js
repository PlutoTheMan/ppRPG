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
    }

    make_grid_divs_and_set_dataset(){
        console.log("!")
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