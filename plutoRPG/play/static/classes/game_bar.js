class GameBar{
    constructor() {
        this.bar_top_html = document.getElementById("game_bar")
        this.bar_left_html = document.getElementById("game_bar_left")
        this.init()
        this.update()
    }

    init(){
        this.bar_top_html.classList.remove("hidden")
        this.bar_left_html.classList.remove("hidden")
    }

    update(){
        this.bar_top_html.style.width = `${square_size_base*game_view_multiplier * (x_squares)}px`
        this.bar_top_html.style.height = `${square_size_base*game_view_multiplier}px`

        this.bar_left_html.style.width = `${square_size_base*game_view_multiplier}px`
        this.bar_left_html.style.height = `${square_size_base*game_view_multiplier * (y_squares - 2)}px`
        this.bar_left_html.style.top = `${square_size_base*game_view_multiplier}px`
        this.bar_left_html.style.marginLeft =
            `${(div_content.offsetWidth - square_size_base*game_view_multiplier) / 2 - Math.floor(x_squares/2)*square_size_base*game_view_multiplier}px`

    }
}