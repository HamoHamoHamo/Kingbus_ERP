const RouteListHBodyTr = document.querySelectorAll(".RouteListHBodyTr")
const RouteListTBody = document.querySelector(".RouteListTBody")


// 선택노선 최상단으로 이동, 색 변경, 클래스 추가
function selectRoute() {
    if (parms.has("id")) {
        for (i = 0; i < RouteListHBodyTr.length; i++) {
            if (RouteListHBodyTr[i].classList[1] == parms.get("id")) {
                RouteListHBodyTr[i].classList.add("selectRoute")
            }
        }
    }
}