const RouteListHBodyTr = document.querySelectorAll(".RouteListHBodyTr")
const RouteListTBody = document.querySelector(".RouteListTBody")


// 선택노선 최상단으로 이동, 색 변경, 클래스 추가
function selectRoute() {
    if (window.location.search !== "") {
        let queryId = window.location.search.split("id=")[1].split("&")[0]
        if (queryId !== "") {
            for (i = 0; i < RouteListHBodyTr.length; i++) {
                if (RouteListHBodyTr[i].classList[1] == queryId) {
                    RouteListHBodyTr[i].classList.add("selectRoute")
                }
            }
            groupList.style.display = "none"
            schedule.style.display = "flex"
            sideLayoutOpenBox.style.display = "none"
            sideLayout.style.width = "36rem"
            mainLayout.style.width = "calc(100% - 38rem)"
        }
    }
}



// selectRoute클래스 여부 확인 -> 배차가능
function dispatchAble() {
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].classList.contains("selectRoute")) {
        }
    }
}
