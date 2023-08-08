const host = window.location.host
const url = `ws://${host}/ws/socket-server/`

var gameSocket

function make_websocket_connection(url){
    return new WebSocket(url)
}

// Is handler a good name?
function get_handlers(socket) {
    socket.onmessage = function(e){
        let data = JSON.parse(e.data)
        // console.log('Data:', data)

        if (data.type == 'chat'){
            game_chat.log_message(data.author, data.message, data.context)
            if (data.msg_context == "disconnect"){
                worldmap.disconnect_player(data.disconnected_player)
            }
        } else if (data.type == 'move'){
            main_player.move(data.message, data.view)
        } else if (data.type == 'view'){
            worldmap.draw_ground_and_player(JSON.parse(data['view']))
            worldmap.draw_ground_layer(JSON.parse(data['view']), 1)
        } else if (data.type == 'view_player_movement'){
            console.log("from_movement")
            worldmap.draw_from_view_player_movement(JSON.parse(data['view']))
        } else if (data.type == "item_drag"){
            console.log("Item Drag...")
        } else if (data.type == "experience_gain"){
            let exp = parseInt(data.data_experience)
            let levels = parseInt(data.data_levels)
            main_player.add_experience(exp)
            if (levels != 0){
                main_player.add_level(levels)
            }
            console.log(`got experience: ${exp}`)
        } else if (data.type == "command_err"){
            console.log(`command error: ${data.data}`)
        } else if (data.type == "commands_list"){
            console.log(`available commands: ${data.data}`)
        } else if (data.type == "experience_required_for_level"){
            console.log(`experience needed: ${data.data}`)
        } else if (data.type == "level_limit_change"){
            let exp_min = parseInt(data.data_exp_min)
            let exp_max = parseInt(data.data_exp_max)
            game_bar.updateProgress(game_bar.bar_level,
                main_player.exp_required_for_this_level,
                main_player.exp_required_for_next_level,
                main_player.experience
            )
            main_player.exp_required_for_this_level = exp_min
            main_player.exp_required_for_next_level = exp_max
        }
    }

    socket.onclose = function(e){
        console.log("Connection lost...")
    }
}

async function require_socket_connection(){
    gameSocket = make_websocket_connection(url)

    return new Promise((resolve) => {
        setTimeout(() => {
          resolve();
        }, 100);
      });
}
