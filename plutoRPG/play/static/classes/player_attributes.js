class PlayerAttributes{
    constructor() {
        console.log("Creating PlayerAttributes instance")
        this.html_element = document.getElementById("player_attributes")
        this.htlm_element_starting_width = square_width * 5
        this.init()
        this.active = null
        this.add_event_listener()
    }

    init(){
        if (this.html_element.classList.contains("hidden")){
            this.active = false
        } else {
            this.active = true
        }

        this.html_element.style.maxWidth = `${this.htlm_element_starting_width}px`
        document.getElementById("attr_name").innerText = main_player.name
        document.getElementById("attr_vocation").innerText = main_player.vocation_to_name(main_player.vocation)
        document.getElementById("attr_experience").innerText = main_player.experience
        document.getElementById("attr_level").innerText = main_player.level

        document.getElementById("attr_skill_fist").innerText = main_player.skills.fist
        document.getElementById("attr_skill_club").innerText = main_player.skills.club
        document.getElementById("attr_skill_sword").innerText = main_player.skills.sword
        document.getElementById("attr_skill_axe").innerText = main_player.skills.axe
        document.getElementById("attr_skill_shielding").innerText = main_player.skills.shielding
        // this.html_element.style.width = 300 + "px"
        // this.html_element.style.maxWidth = 300 + "px"
    }

    update_level(){
        document.getElementById("attr_level").innerText = main_player.level
    }
    update_experience(){
        document.getElementById("attr_experience").innerText = main_player.experience
    }
    hide(){
        this.active = false
        if (!this.html_element.classList.contains("hidden")){
            this.html_element.classList.add("hidden")
        }
    }

    show(){
        this.active = true
        if (this.html_element.classList.contains("hidden")){
            this.html_element.classList.remove("hidden")
        }
    }
    toggle(){
        if (!this.html_element.classList.contains("hidden")){
            this.hide()
        } else {
            this.show()
        }
    }
    add_event_listener(){
        let context = this
        window.addEventListener("keydown", function (e){
            if (e.key == "c" && !game_chat.active){
                context.toggle()
            } else if (e.key == "Escape" && !game_chat.active){
                context.hide()
            }
        })
    }
}