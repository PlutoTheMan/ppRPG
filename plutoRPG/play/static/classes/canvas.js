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
const game_bar = document.querySelector("#game_bar")
const game_grid = document.getElementById("game_grid")
const content_wrap = document.querySelector(".content_wrap")

const x_squares = 11
const y_squares = 11

const game_view_multiplier = 2
const game_width = 32*x_squares*game_view_multiplier
const game_height = 32*y_squares*game_view_multiplier

const screen_width = game_width - 32*2*game_view_multiplier
const screen_height = game_height - 32*2*game_view_multiplier

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

game_bar.style.width = `${game_width}px`
game_bar.style.height = `${square_height}px`

content_wrap.style.width = `${game_width - square_width*2}px`
content_wrap.style.height = `${game_height - square_height*2}px`


const html_characters_list = document.querySelector(".character_list")