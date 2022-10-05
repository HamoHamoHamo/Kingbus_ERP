const routeItem = document.querySelectorAll(".routeItem")
const RouteListHBodyTr = document.querySelectorAll(".RouteListHBodyTr")


window.onload = function () {
    // for (i = 0; i < RouteListHBodyTr.length; i++) {
    //     if (window.location.search.split("id")[1].split("&")[0] == RouteListHBodyTr[i].classList[1]) {
    //         RouteListHBodyTr[i].style.order = "1"  //table로 되어있어 순서 변경이 안됨
    // 1.방법을 따로 찾기
    // 2.div로 변경
    // 3.태환이가 하게하기
    //         RouteListHBodyTr[i].style.backgroundColor = "#29b68b"
    //     }
    // }
}


for (i = 0; i < routeItem.length; i++) {
    routeItem[i].addEventListener("click", loadRoute)
}

function loadRoute() {
    // location.href = `${window.location.split("?")[0]}?id=${this.classList[1]}${window.location.search.split("?")[1]}`
}



for (i = 0; i < routeItem.length; i++) {
    RouteListHBodyTr[i].addEventListener("click", loadRouteList)
}

function loadRoute() {
    // location.href = `${window.location.split("?")[0]}?id=${this.classList[1]}${window.location.search.split("?")[1]}`
}