const RouteListScroll = document.querySelector(".RouteListScroll")
const route = document.querySelectorAll(".RouteListBodyTr")


window.onload = function () {
    let parms = new URLSearchParams(location.search)
    addComma()
    visivleFix()
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
}