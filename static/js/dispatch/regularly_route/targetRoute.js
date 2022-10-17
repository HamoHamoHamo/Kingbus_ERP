const RouteListScroll = document.querySelector(".RouteListScroll")
const route = document.querySelectorAll(".RouteListBodyTr")


window.onload = function () {
    addComma()
    visivleFix()
    for (i = 0; i < route.length; i++) {
        if (route[i].classList.contains(`${window.location.search.split("height=")[1].split("&")[0]}`)) {
            route[i].style.backgroundColor = "#CDCDCE"
        }
    };
    if (window.location.search.split("height=")[1].split("&")[0] > 10) {
        RouteListScroll.scrollTop = (window.location.search.split("height=")[1].split("&")[0] - 9) * 43
    }
    if(window.location.search.split("close=")[1]){
        groupClose()
    }
}