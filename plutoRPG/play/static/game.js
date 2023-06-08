const canvas = document.getElementById("canvas_game")
const ctx = canvas.getContext("2d")
ctx.imageSmoothingEnabled= false



const canvas_players = document.getElementById("canvas_players")
const ctx_players = canvas_players.getContext("2d")
ctx_players.imageSmoothingEnabled= false

const canvas_ground = document.getElementById("canvas_ground")
const ctx_ground = canvas_ground.getContext("2d")
ctx_ground.imageSmoothingEnabled= false

const canvas_items = document.getElementById("canvas_items")
const ctx_items = canvas_items.getContext("2d")
ctx_items.imageSmoothingEnabled= false

const character_ui = document.querySelector(".character_list")

const game_grid = document.getElementById("game_grid")
const content_wrap = document.querySelector(".content_wrap")

const x_squares = 11
const y_squares = 11

const game_view_multiplier = 2
const game_width = 32*x_squares*game_view_multiplier
const game_height = 32*y_squares*game_view_multiplier

const inventory = document.getElementById("inventory")

canvas.width = canvas_players.width = canvas_ground.width = canvas_items.width = game_width
canvas.height = canvas_players.height =  canvas_ground.height = canvas_items.height = game_height
game_grid.style.width = `${game_width}px`
game_grid.style.height = `${game_height}px`
character_ui.style.height = `${game_height}px`
character_ui.style.width = `${game_width}px`
inventory.style.width = `${game_width/3}px`
inventory.style.height = `${game_height}px`

const square_width = Math.round(canvas.width / x_squares)
const square_height = Math.round(canvas.height / y_squares)

content_wrap.style.width = `${game_width - square_width*2}px`
content_wrap.style.height = `${game_height - square_height*2}px`


const html_characters_list = document.querySelector(".character_list")


const players = []
const items = {}

let main_player = ""
let screen = ""
let player_inventory = ""
let worldmap = ""
let game_chat = ""


async function getCharacters() {
    const response = await fetch("get_characters");
    return response
}

async function get_map_tile_sets() {
    const response = await fetch("get_map_tile_sets");
    return response
}


async function selectCharacter(name){
    await require_socket_connection()
    get_handlers(gameSocket)
    const response = await fetch(`select_character/${name}`);
    return response
}

get_map_tile_sets().then((response)=>response.json()).then((data)=>{
    sprite_list = data
    // console.log(data)
})

getCharacters().then((response)=>response.json()).then((data)=>{
    data.forEach(character=>{
        const li = document.createElement("li");
        li.setAttribute("data", character[0])
        li.innerText = `${character[0]} (level ${character[1]} ${character[3] ? 'logged in' : 'logged out'})`
        li.addEventListener("click", e=>{
            selectCharacter(e.target.getAttribute("data")).then(
                (response)=>response.json()).then((data)=>{
                if (data['accepted']){
                    console.log("Choosing character succeded.")
                    // console.log(data.content.bag)
                    loadGame(data.content)
                } else {
                    console.log(data.error_msg)
                }
            })
        })
        html_characters_list.append(li)
    })
})

let dragged_from = {x:0, y:0}
let dragged_to = {x:0, y:0}

function drawMapMesh(){

    const game_grid = document.getElementById("game_grid")
    for (let y=1; y <= y_squares; y++){
        for (let x=1; x <= x_squares; x++){
            const div = document.createElement("div")

            div.classList.add('border-inner-grid', 'inline-block', 'm-0', 'p-0')
            // For easy navigation on drag etc.
            div.dataset.x = (x-1).toString()
            div.dataset.y = (y-1).toString()
            div.style.width = `${square_width}px`
            div.style.height = `${square_height}px`

            div.addEventListener("drag", event=>{
                // dragged_from = {x: event.target.dataset.x, y: event.target.dataset.y}
                dragged_from = screen.grid_tile_cord_to_real_pos({x: event.target.dataset.x, y: event.target.dataset.y})
                event.preventDefault()
            })

            div.addEventListener("dragenter", event=>{
                event.target.classList.add("dragenter")
                main_player.inventory.drag_destination_type = "ground"

                // console.log({x: event.target.dataset.x, y: event.target.dataset.y})
                // Translating selected grid pos to real server pos..
                dragged_to = screen.grid_tile_cord_to_real_pos({x: event.target.dataset.x, y: event.target.dataset.y})
                event.preventDefault()
            })

            div.addEventListener("dragstart", event=>{
                main_player.inventory.drag_source_type = "ground"
            })

            div.addEventListener("dragleave", event=>{
                event.target.classList.remove("dragenter")
                event.preventDefault()
            })

            div.addEventListener("dragend", event=>{
                // console.log(main_player.inventory.drag_destination_type)
                main_player.drag_drop(
                    main_player.inventory.drag_source_type,
                    main_player.inventory.drag_destination_type
                )

                event.preventDefault()
            })

            game_grid.append(div)
            if (x==x_squares){
                div.classList.add('border-last-right')
            }

            if (y==y_squares){
                div.classList.add('border-last-bottom')
            }

        }

        // ctx.moveTo(x, 0)
        // ctx.lineTo(x, canvas.height)
    }



    ctx.stroke()
}



function loadGame(content){
    html_characters_list.remove()
    drawMapMesh()
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
    window.requestAnimationFrame(animate)
}

function animate() {
    // console.log(players)
    main_player.update()
    // main_player.draw()
    window.requestAnimationFrame(animate);
}

