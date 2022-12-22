const RouteList = document.querySelector(".RouteList")
const dispatchDeletBtn = document.querySelector(".dispatchDeletBtn")
const allChecker = document.querySelector(".allChecker")

dispatchDeletBtn.addEventListener("click", deleteDispatch)

function deleteDispatch() {
    RouteList.action = "regularly/connect/delete"
    let deleteArr = []
    let deleteCounter = 0
    let parms = new URLSearchParams(location.search)
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].children[0].children[0].checked) {
            if (RouteListHBodyTr[i].classList[1] === parms.get("id")) {
                deleteArr.push(RouteListHBodyTr[i].children[4].children[0].value !== "" ? true : false)
            } else {
                deleteArr.push(RouteListHBodyTr[i].children[4].innerText !== "" ? true : false)
            }
        }
    };
    for (i = 0; i < deleteArr.length; i++) {
        if (!deleteArr[i]) {
            deleteCounter++
        }
    };
    // if (deleteCounter === deleteArr.length) {
    //     return alert("삭제할 배차가 없습니다.")
    // } else {
    //     RouteList.submit();
    // }
    RouteList.submit();
}