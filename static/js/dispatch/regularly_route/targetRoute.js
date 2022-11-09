const RouteListScroll = document.querySelector(".RouteListScroll")
const route = document.querySelectorAll(".RouteListBodyTr")
const inputSelect = document.querySelector(".inputSelect")
const routeListsearch = document.querySelector("#routeListsearch")


window.onload = function () {
    let parms = new URLSearchParams(location.search)
    addComma()
    for (i = 0; i < route.length; i++) {
        if (route[i].classList.contains(`${parms.get("height")}`)) {
            route[i].style.backgroundColor = "#CDCDCE"
        }
    };
    if (parseInt(parms.get("height")) > 10) {
        RouteListScroll.scrollTop = (parseInt(parms.get("height")) - 9) * 43
    }
    if(parseInt(parms.get("close"))){
        groupClose()
    }
    if(parms.has("group")){
        for (i = 0; i < inputSelect.children.length; i++){
            if(inputSelect.children[i].value === parms.get("group")){
                return inputSelect.children[i].selected = true
            }
        };
    }
    if(parms.has("search")){
        routeListsearch.value = parms.get("search")
    }
}