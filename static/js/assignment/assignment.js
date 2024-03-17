const assignmentConnectSaveBtn = document.querySelector(".assignmentConnectSaveBtn")

assignmentConnectSaveBtn.addEventListener("click", assignmentConnectSave)

function assignmentConnectSave() {
    let bus = ""
    let driver = ""
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].children[0].children[0].checked) {
            bus = useVehicle ? RouteListHBodyTr[i].children[4].children[1].value : ""
            driver = RouteListHBodyTr[i].children[5].children[0].value
        }
    };
    if (driver == "") {
        alert("직원을 선택해 주세요")
    } else if (bus == "" && useVehicle) {
        alert("차량을 선택해 주세요")
    } else {
        RouteList.submit();
    }
}

// connect delete
const RouteList = document.querySelector(".RouteList")
const dispatchDeletBtn = document.querySelector(".dispatchDeletBtn")
const allChecker = document.querySelector(".allChecker")

dispatchDeletBtn.addEventListener("click", deleteConnect)

function deleteConnect() {
    RouteList.action = connectDeleteUrl
    // let deleteArr = []
    // let deleteCounter = 0
    // let parms = new URLSearchParams(location.search)
    // for (i = 0; i < RouteListHBodyTr.length; i++) {
    //     if (RouteListHBodyTr[i].children[0].children[0].checked) {
    //         if (RouteListHBodyTr[i].classList[1] === parms.get("id")) {
    //             deleteArr.push(RouteListHBodyTr[i].children[4].children[0].value !== "" ? true : false)
    //         } else {
    //             deleteArr.push(RouteListHBodyTr[i].children[4].innerText !== "" ? true : false)
    //         }
    //     }
    // };
    // for (i = 0; i < deleteArr.length; i++) {
    //     if (!deleteArr[i]) {
    //         deleteCounter++
    //     }
    // };
    // if (deleteCounter === deleteArr.length) {
    //     return alert("삭제할 배차가 없습니다.")
    // } else {
    //     RouteList.submit();
    // }
    RouteList.submit();
}