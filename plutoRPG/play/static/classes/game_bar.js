class GameBar{
    constructor() {
        this.bar_top_html = document.getElementById("game_bar")
        this.bar_left_html = document.getElementById("game_bar_left")
        this.bar_level = document.getElementById("bar_progress_level")
        this.init()
        this.update()
    }

    init(){
        this.bar_top_html.classList.remove("hidden")
        this.bar_left_html.classList.remove("hidden")
    }

    updateProgress(element, minValue, maxValue, currentValue) {
        console.log(minValue)
        console.log(maxValue)
        console.log(currentValue)
      if (!(element instanceof HTMLElement)) {
        return null;
      }
      if (
        typeof minValue !== 'number' ||
        typeof maxValue !== 'number' ||
        typeof currentValue !== 'number'
      ) {
        return null;
      }
      if (minValue > maxValue) {
        return null;
      }

      let percentage = ((currentValue - minValue) / (maxValue - minValue)) * 100
      percentage = Math.min(Math.max(percentage, 0), 100)

      element.style.width = percentage + '%'
      const green = Math.round(percentage * 2.55)
      const red = 255 - green
      element.style.backgroundColor = `rgb(${red}, ${green}, 0)`

      return percentage;
    }

    update(){
        this.bar_top_html.style.width = `${square_size_base*game_view_multiplier * (x_squares)}px`
        this.bar_top_html.style.height = `${square_size_base*game_view_multiplier}px`

        this.bar_left_html.style.width = `${square_size_base*game_view_multiplier}px`
        this.bar_left_html.style.height = `${square_size_base*game_view_multiplier * (y_squares - 2)}px`
        this.bar_left_html.style.top = `${square_size_base*game_view_multiplier}px`
        this.bar_left_html.style.marginLeft =
            `${(div_content.offsetWidth - square_size_base*game_view_multiplier) / 2 - Math.floor(x_squares/2)*square_size_base*game_view_multiplier}px`

    }
}