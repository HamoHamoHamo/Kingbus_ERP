const driverTd = document.querySelectorAll(".driverTd")
const RouteListScrollBody = document.querySelector(".RouteListScrollBody")

window.onload = function () {
    let parms = new URLSearchParams(location.search)
    inputToDay()
    selectRoute()
    drawSchdule()
    // notPairFilter()
    if (parms.has("id")) {
        DispatcBusFilterRegularly()
        afterSelectRoute()
    }
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].classList.contains("selectRoute") && window.location.search.split("height=")[1].split("&")[0] > 10) {
            RouteListScrollBody.scrollTop = (window.location.search.split("height=")[1].split("&")[0] - 10) * 36
        };
    }
}