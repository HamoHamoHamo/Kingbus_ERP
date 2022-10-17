const driverTd = document.querySelectorAll(".driverTd")
const RouteListScrollBody = document.querySelector(".RouteListScrollBody")

window.onload = function () {
    inputToDay()
    selectRoute()
    dispatchAble()
    drawSchdule()
    notPairFilter()
    if (window.location.search !== "") {
        if (window.location.search.split("id")[1].split("&")[0] !== "") {
            DispatcBusFilterRegularly()
        }
    }
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].classList.contains("selectRoute") && window.location.search.split("height=")[1] > 10) {
            RouteListScrollBody.scrollTop = (window.location.search.split("height=")[1] - 10) * 36
        };
    }
}