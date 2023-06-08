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
            console.log(JSON.parse(data['view']))
        } else if (data.type == 'view_player_movement'){
            worldmap.draw_from_view_player_movement(JSON.parse(data['view']))
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
