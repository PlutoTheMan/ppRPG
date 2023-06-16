class Settings {
    constructor() {
        this.active = false
        this.html = document.getElementById("game_options")
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