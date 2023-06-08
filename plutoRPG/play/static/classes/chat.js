class Chat{
    constructor() {
        this.active = false
        this.chat_box = document.getElementById("chat_box")
        this.chat_input = document.createElement('input')
        this.message_box = document.getElementById('messages')
        this.form = document.createElement('form')
        this.init()
        this.listener = null
    }

    init(){
        this.html_create_and_append()
        this.add_chat_close_functionality()
        this.init_listener()
    }

    add_chat_close_functionality(){
        let context = this
        document.querySelector("#chat-btn-close").onclick = function(){
            context.cancel_message()
            context.deactivate()
            context.hide()
        }
    }
    log_message(author, msg, context) {
        const p = document.createElement("p")

        let curr_date = new Date()
        const span_date = document.createElement("span")
        span_date.classList.add("font-bold", "text-orange-700", "mr-1")
        span_date.innerText = ("0" + curr_date.getHours().toString()).slice(-2) + ":" +
            ("0" + curr_date.getMinutes().toString()).slice(-2)

        const span_author = document.createElement("span")
        span_author.classList.add("font-bold", "text-neutral-200")
        span_author.innerText = author

        const span_message = document.createElement("span")
        if (context == "")
            span_message.classList.add("font-bold", "text-neutral-300")
        else if (context == "disconnect")
            span_message.classList.add("font-bold", "text-red-500")
        else if (context == "connect")
            span_message.classList.add("font-bold", "text-green-500")
        span_message.innerText = ": " + msg

        p.classList.add("px-2", "bg-slate-500/80")
        p.append(span_date)
        if (author != "Server")
            p.append(span_author)
        p.append(span_message)

        this.message_box.insertBefore(p, this.message_box.firstChild)
        // this.message_box.append(p)
    }

    send_message(){
        let message = this.form.message.value

        gameSocket.send(JSON.stringify(
            {'message': message}
        ))

        this.form.reset()
    }

    cancel_message() {
        this.form.reset()
    }
    init_listener(){
        let context = this
        this.listener = window.addEventListener("keydown", function(e){
            switch(e.key) {
                case "Enter":
                    if (!context.is_active()){
                        context.show()
                        context.activate()
                        context.chat_input.focus()
                    } else {
                        context.deactivate()
                        context.chat_input.blur()
                        context.send_message()
                    }
                    break
                case "Escape":
                    context.cancel_message()
                    context.deactivate()
                    context.hide()
                    context.chat_input.blur()
                    break
            }
        })
    }

    activate(){
        this.active = true
    }

    show(){
        if (this.chat_box.classList.contains("hidden"))
            this.chat_box.classList.remove("hidden")
    }
    deactivate(){
        this.active = false

    }

    hide(){
        if (!this.chat_box.classList.contains("hidden"))
            this.chat_box.classList.add("hidden")
    }

    is_active(){
        if (this.active)
            return true
        return false
    }

    toggle_chat(){
        if (this.is_active())
            this.deactivate()
        else
            this.activate()
    }
    html_create_and_append() {
        const context = this

        this.chat_box.setAttribute("style", `width: ${game_width}px`)

        this.form.setAttribute('id', 'chat')
        this.form.classList.add("my-2")

        this.chat_input.setAttribute("type", "text")
        this.chat_input.setAttribute("name", "message")
        this.chat_input.setAttribute("maxlength", "100")

        this.form.addEventListener('submit', (e)=>{
            e.preventDefault()
        })

        this.chat_input.addEventListener('click', (e)=>{
            e.preventDefault()
            context.activate()
        })

        this.form.appendChild(this.chat_input)
        this.chat_box.append(this.form)
    }
}
