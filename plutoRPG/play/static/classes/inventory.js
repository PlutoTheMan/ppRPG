class Inventory {
    constructor(bag=null) {
        this.html_element = document.getElementById("inventory")
        this.inventory_starting_width = game_width/3 + "px"
        this.left_hand = null
        this.right_hand = null
        this.legs = null
        this.boots = null
        this.belt = null
        this.ring = null
        this.amulet = null
        this.bag = bag
        this.slots = {
            0: null,
            1: null,
            2: null,
            3: null,
            4: null,
        }

        this.open = false
        this.init()
        this.dragging = false
        this.dragged_from = null
        this.dragged_to = null

        this.mouse_on_inventory_id = null

        this.drag_source = null
        this.drag_source_type = null
        this.drag_destination_type = null
        this.drag_destination = null

        this.mouse_on_inventory = false
    }

    init(){
        // Make all the bags content dragable
        let bags = document.querySelector(".bag").children
        let context = this
        // Skip <p> tag
        bags[0].remove()
        Array.from(bags).forEach(bag=>{
            let target_element = bag.children[0]
            context.put_blank_image(target_element)

            bag.addEventListener("mouseenter", function(e){
                context.mouse_on_inventory = true
                context.mouse_on_inventory_id = e.target.dataset.id
                ground.mouse_on_ground = false
            })

            // bag.addEventListener("dragstart", event=>{
            //     // console.log(event.target.parentElement.dataset.id)
            //     context.dragged_source = event.target.parentElement.dataset.id
            //     context.drag_source_type = "inventory"
            //
            //     context.dragging = true
            //     event.dataTransfer.setDragImage(ghost_image, 0, 0)
            //     event.target.classList.add("bg-slate-300")
            // })
            //
            // bag.addEventListener("dragenter", event=>{
            //     context.drag_destination = event.target.parentElement.dataset.id
            //     context.drag_destination_type = "inventory"
            // })

            // bag.children[0].addEventListener("dragend", event=>{
            //     context.dragging = false
            //     main_player.drag_drop(
            //         main_player.inventory.drag_source_type,
            //         main_player.inventory.drag_destination_type
            //     )
            //     event.target.classList.remove("bg-slate-300")
            // })
            //
            //
            // bag.children[0].addEventListener("drag", event=>{
            //     event.dataTransfer.setDragImage(ghost_image, 0, 0);
            // })
        })
        this.update()
    }

    put_blank_image(element){
        console.log(element)
        element.setAttribute("src", "/static/sprites/ghost_image.png")
        element.style.width = 64 + "px"
        element.style.left = 32 + "px"
        element.style.top = 32 + "px"
    }
    update(){
        console.log("UPDATING")
        for (let bag_slot in this.bag) {
            let g_id = this.bag[bag_slot]['game_id']
            console.log(g_id)
            let bag_class = ".bag_" + (g_id - 1).toString()

            let img = document.querySelector(bag_class).children[0]
            // img.source = "/static/sprites/weapons.png"
            img.setAttribute("src", "/static/sprites/weapons.png")
            img.style = ""
            let left = ((g_id-1 % 4)*64)%256 - 64
            // -1 at the end of top position to fix pixel bug
            let top = Math.floor(g_id / 5) * 64 - 64 - 1
            img.style.left = `${-left}px`
            img.style.top = `${-top}px`
        }
    }
    is_open(){
        if (this.open){
            return true
        }
        return false
    }

    toggle(){
        if (!this.open){
            this.html_element.style.maxWidth = this.inventory_starting_width
            this.open = true
            this.html_element.classList.add("inventory-border")
        } else {
            this.html_element.style.maxWidth = 0 + "px"
            this.open = false
            this.html_element.classList.remove("inventory-border")
        }
    }
}