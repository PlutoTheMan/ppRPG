const players = []
const items = {}

let main_player = null
let screen = null
let player_inventory = null
let worldmap = null
let game_chat = null
let ground = null
let mouse = null
let game_settings = null

async function get_characters() {
    const response = await fetch("get_characters");
    return response
}
async function get_map_tile_sets() {
    const response = await fetch("get_map_tile_sets");
    return response
}
async function select_character(name){
    await require_socket_connection()
    get_handlers(gameSocket)
    const response = await fetch(`select_character/${name}`);
    return response
}

get_map_tile_sets().then((response)=>response.json()).then((data)=>{
    sprite_list = data
    // console.log(data)
})
get_characters().then((response)=>response.json()).then((data)=>{
    data.forEach(character=>{
        const li = document.createElement("li");
        li.setAttribute("data", character[0])
        li.innerText = `${character[0]} (level ${character[1]} ${character[3] ? 'logged in' : 'logged out'})`
        li.addEventListener("click", e=>{
            select_character(e.target.getAttribute("data")).then(
                (response)=>response.json()).then((data)=>{
                if (data['accepted']){
                    console.log("Choosing character succeded.")
                    // console.log(data.content.bag)
                    load_game(data.content)
                } else {
                    console.log(data.error_msg)
                }
            })
        })
        html_characters_list.append(li)
    })
})
function load_game(content){
    html_characters_list.remove()
    // drawMapMesh()
    worldmap = new Worldmap()
    screen = new Screen()
    player_inventory = new Inventory(content.bag)

    main_player = new MainPlayer({
        player_info: content,
        // equipment =
        inventory: player_inventory
    })
    worldmap.screen = screen

    game_chat = new Chat()
    ground = new Ground()
    mouse = new Mouse()
    game_settings = new Settings()
    game_bar.classList.remove("hidden")
    window.requestAnimationFrame(animate)
}
function animate() {
    main_player.update()
    window.requestAnimationFrame(animate);
}

