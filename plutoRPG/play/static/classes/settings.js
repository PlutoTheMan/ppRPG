class Settings {
    constructor() {
        this.active = false
        this.html = document.getElementById("game_options")
        this.settings_square_size_option = 1

        this.draw_map_mesh_html = document.getElementById("draw_map_mesh")
        this.draw_ground_info_html = document.getElementById("draw_ground_info")

        this.draw_ground_id = false
        this.draw_map_mesh = false

        this.init()
    }

    init(){
        let context = this
        let game_bar_settings = document.getElementById('game_bar_settings')
        game_bar_settings.addEventListener("click", this.toggle, false)
        this.html.setAttribute("style",`width:${game_width}px`);
        this.html.setAttribute("style",`height:${screen_height}px`);
        this.html.style.width=`${game_width}px`;
        this.html.style.height=`${screen_height}px`;

        let options_square_size = document.querySelector("#game_options_display").querySelectorAll("button")
        options_square_size.forEach(function(e, i){
            e.dataset.option = i.toString()
            e.dataset.value = ((i+1)*square_size_base).toString()
            e.addEventListener("click", function (){
                context.select_square_size(i)
                // console.log(this)
            })
        })
        this.select_square_size(this.settings_square_size_option)

        this.draw_map_mesh_html.addEventListener("click", function(e){
            if (!e.target.checked) {
                ground.grid_remove_mesh()
            } else {
                ground.grid_add_mesh()
            }
        })

        if (!context.draw_map_mesh) {
            ground.grid_remove_mesh()
        }

        this.draw_ground_info_html.addEventListener("click", function(e){
            if (!e.target.checked) {
                context.draw_ground_id = false
            } else {
                context.draw_ground_id = true
            }
        })


    }

    select_square_size(i){
        let current_element = document.querySelector("#game_options_display")
            .querySelector(`[data-option="${this.settings_square_size_option.toString()}"]`)
        if (current_element.classList.contains("options_square_size_selected")){
            current_element.classList.remove("options_square_size_selected")
            current_element.classList.add("options_square_size_not_selected")
        }

        this.settings_square_size_option = i
        let target_element = document.querySelector("#game_options_display")
            .querySelector(`[data-option="${i.toString()}"]`)
        target_element.classList.add("options_square_size_selected")
        // console.log(i)
        game_view_multiplier = i+1

        game_width = square_size_base*x_squares*game_view_multiplier
        game_height = square_size_base*y_squares*game_view_multiplier
        screen_width = game_width - square_size_base*2*game_view_multiplier
        screen_height = game_height - square_size_base*2*game_view_multiplier

        square_width = square_size_base * game_view_multiplier
        square_height = square_size_base * game_view_multiplier

        screen.update_canvas_styles()
        game_bar.update()
        main_player.update_draw_pos()
        ground.update_grid_divs()
    }
    toggle(){
        // Using game_settings instead of this, because of event listener on click context
        if (game_settings.active){
            game_settings.disable()
        } else {
            game_settings.enable()
        }
    }

    enable(){
        this.active = true
        this.html.classList.remove("hidden")
    }

    disable(){
        this.active = false
        this.html.classList.add("hidden")
    }
}