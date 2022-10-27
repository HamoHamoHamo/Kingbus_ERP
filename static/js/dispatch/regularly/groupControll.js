const groupListItem = document.querySelectorAll(".groupOpen")

for (i = 0; i < groupListItem.length; i++) {
    groupListItem[i].addEventListener("click", openGroup)
}

function openGroup() {
    const innerRouteItem = this.parentNode.parentNode.querySelectorAll(".routeItem")
    if (this.classList.contains("openGroup")) {
        this.classList.remove("openGroup")
        for (i = 0; i < innerRouteItem.length; i++) {
            innerRouteItem[i].style.display = "none"
        }
    } else {
        this.classList.add("openGroup")
        for (i = 0; i < innerRouteItem.length; i++) {
            innerRouteItem[i].style.display = "flex"
        }
    }
}