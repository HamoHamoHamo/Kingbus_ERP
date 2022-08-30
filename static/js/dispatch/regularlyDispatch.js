const dispatchRouteBus = document.querySelectorAll(".listTable tbody td:nth-child(3)")
const dispatchRouteDriver = document.querySelectorAll(".listTable tbody td:nth-child(4)")
const dispatchRouteSpare = document.querySelectorAll(".listTable tbody td:nth-child(5)")

for (i = 0; i < dispatchRouteBus.length; i++) {
    dispatchRouteBus[i].addEventListener("click", dispatchCheck)
}

function dispatchCheck() {
    if (!this.classList.contains("checkBus")) {
        for (i = 0; i < dispatchRouteBus.length; i++) {
            dispatchRouteBus[i].classList.remove("checkBus")
            dispatchRouteBus[i].style.backgroundColor = "transparent"
            dispatchRouteBus[i].parentNode.children[3].style.backgroundColor = "transparent"
            dispatchRouteBus[i].parentNode.children[4].style.backgroundColor = "transparent"
        }
        this.style.backgroundColor = "#0069D9"
        this.parentNode.children[3].style.backgroundColor = "#0069D9"
        this.parentNode.children[4].style.backgroundColor = "#0069D9"
        this.classList.add("checkBus")
    } else {
        this.classList.remove("checkBus")
        this.style.backgroundColor = "transparent"
        this.parentNode.children[3].style.backgroundColor = "transparent"
        this.parentNode.children[4].style.backgroundColor = "transparent"
    }
}