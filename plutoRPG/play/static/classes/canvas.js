const square_size_base = 32
const x_squares = 11
const y_squares = 11

const canvas = document.getElementById("canvas_game")
const ctx = canvas.getContext("2d")

let game_view_multiplier = 2

let game_width = square_size_base*x_squares*game_view_multiplier
let game_height = square_size_base*y_squares*game_view_multiplier
let screen_width = game_width - square_size_base*2*game_view_multiplier
let screen_height = game_height - square_size_base*2*game_view_multiplier
let square_width = square_size_base * game_view_multiplier
let square_height = square_size_base * game_view_multiplier



ctx.imageSmoothingEnabled= false
const canvas_players = document.getElementById("canvas_players")
const ctx_players = canvas_players.getContext("2d")

ctx_players.imageSmoothingEnabled= false
const div_content = document.querySelector(".content")
const canvas_ground = document.getElementById("canvas_ground")
const ctx_ground = canvas_ground.getContext("2d")

ctx_ground.imageSmoothingEnabled= false
const canvas_items = document.getElementById("canvas_items")
const ctx_items = canvas_items.getContext("2d")

ctx_items.imageSmoothingEnabled= false
const character_ui = document.querySelector(".character_list")
const game_grid = document.getElementById("game_grid")

const content_wrap = document.querySelector(".content_wrap")

const inventory = document.getElementById("inventory")
const html_player_attributes = document.getElementById("player_attributes")

canvas.width = canvas_players.width = canvas_ground.width = canvas_items.width = game_width
canvas.height = canvas_players.height =  canvas_ground.height = canvas_items.height = game_height

character_ui.style.height = `${game_height}px`
character_ui.style.width = `${game_width}px`
inventory.style.width = `${square_width*4}px`
inventory.style.height = `${game_height}px`

html_player_attributes.style.width = `${game_width/2}px`
// html_player_attributes.style.width = `100px`
html_player_attributes.style.height = `${game_height*2}px`


const html_characters_list = document.querySelector(".character_list")