const sheduleLine = document.querySelectorAll(".scheduleTableTr")
const scheduleRadio = document.querySelectorAll(".scheduleRadio")
const scheduleLabel = document.querySelectorAll(".scheduleHeaderFilterBox label")
const routeTimeInput = document.querySelectorAll(".quarterBox input")
const scheduleTableTr = document.querySelectorAll(".scheduleTableTr")


// 노선 운행시간
let routeTimeStart = 0;
let routeTimeEnd = 0;

function getRouteTime() {
    routeTimeStart = parseInt(routeTimeInput[0].value * 60) + parseInt(routeTimeInput[1].value)
    routeTimeEnd = parseInt(routeTimeInput[2].value * 60) + parseInt(routeTimeInput[3].value)
}



// 요일변경
for (i = 0; i < scheduleRadio.length; i++) {
    scheduleRadio[i].addEventListener("change", callSchedule)
}

function callSchedule() {
    deleteSchdule()
    ableToDispatchDelete()
    drawSchdule()
    ableToDispatch()
}


window.onload = function () {
    getRouteTime()
    drawSchdule()
    ableToDispatch()
    dispatchWeekDelete()
    dispatchWeekCheker()
    loadData()
}


// 스케줄 메인
function drawSchdule() {
    // 차량 키 배열
    let dataKey = Object.keys(data)

    if (window.location.search !== "") {

        let driverCount = 0

        for (i = 0; i < dataKey.length; i++) {

            // 기사 오브젝트
            let driverOdj = data[dataKey[i]]
            // 기사 키 배열
            let driverKey = Object.keys(driverOdj)

            for (j = 0; j < driverKey.length; j++) {

                // 노선 오브젝트
                let routeObj = driverOdj[driverKey[j]]
                // 노선 키 배열
                let routeKey = Object.keys(routeObj)



                for (k = 0; k < routeKey.length; k++) {

                    // 요일 오브젝트
                    let weekObj = routeObj[routeKey[k]]
                    // 요일 키 배열
                    let weekKey = Object.keys(weekObj)

                    // 스케줄바 위치, 길이
                    let StartH = parseInt(weekObj[weekKey[1]].substr(0, 2))
                    let EndH = parseInt(weekObj[weekKey[2]].substr(0, 2))
                    let StartM = parseInt(weekObj[weekKey[1]].substr(3, 2))
                    let EndM = parseInt(weekObj[weekKey[2]].substr(3, 2))
                    let startPoint = StartH * 60 + StartM
                    let endPoint = EndH * 60 + EndM
                    let scheduleWidth = (EndH * 60 + EndM) - (StartH * 60 + StartM)


                    // 요일체크
                    let weekChecker = ""
                    for (l = 0; l < scheduleRadio.length; l++) {
                        if (scheduleRadio[l].checked) {
                            weekChecker = scheduleLabel[l].innerText
                        }
                    }


                    //스케줄바 생성
                    if (weekChecker == weekObj[weekKey[5]]) {
                        const startWork = document.createElement('div');
                        if (weekObj[weekKey[0]] == "출근") {
                            startWork.setAttribute("class", "regularlyLineStart");
                        }
                        else {
                            startWork.setAttribute("class", "regularlyLineEnd");
                        }
                        startWork.setAttribute("title", `${weekObj[weekKey[3]]}▶${weekObj[weekKey[4]]}`);
                        startWork.setAttribute("style", `left: ${startPoint * 0.074}rem; width: ${scheduleWidth * 0.074}rem;`);
                        for (l = 0; l < sheduleLine.length; l++) {
                            if (sheduleLine[l].children[12].classList[1] == dataKey[i] && sheduleLine[l].children[12].classList[2] == driverKey[j]) {
                                sheduleLine[l].appendChild(startWork);
                            }
                        }
                        if (endPoint >= routeTimeStart && startPoint <= routeTimeEnd) {
                            for (l = 0; l < sheduleLine.length; l++) {
                                if (sheduleLine[l].children[12].classList[1] == dataKey[i] && sheduleLine[l].children[12].classList[2] == driverKey[j]) {
                                    sheduleLine[l].children[12].classList.add("haveSchedule")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}




// 스케줄 삭제
function deleteSchdule() {
    const scheduleStart = document.querySelectorAll(".regularlyLineStart")
    const scheduleEnd = document.querySelectorAll(".regularlyLineEnd")
    for (i = 0; i < scheduleStart.length; i++) {
        scheduleStart[i].remove()
    }
    for (i = 0; i < scheduleEnd.length; i++) {
        scheduleEnd[i].remove()
    }
}



// 배차가능 차량 초기화

function ableToDispatchDelete() {
    const have = document.querySelectorAll(".haveSchedule")
    const able = document.querySelectorAll(".ableToDispatch")
    for (i = 0; i < have.length; i++) {
        have[i].classList.remove("haveSchedule")
    }
    for (i = 0; i < able.length; i++) {
        able[i].classList.remove("ableToDispatch")
    }
    for (i = 0; i < scheduleTableTr.length; i++) {
        scheduleTableTr[i].classList.remove("scheduleTableTrAble")
        scheduleTableTr[i].classList.remove("scheduleTableTrDisable")
    }
}


// 배차가능 차량
function ableToDispatch() {
    for (i = 0; i < driverTd.length; i++) {
        if (!driverTd[i].classList.contains("haveSchedule")) {
            driverTd[i].classList.add("ableToDispatch")
            driverTd[i].parentNode.classList.add("scheduleTableTrAble")
        } else {
            driverTd[i].parentNode.classList.add("scheduleTableTrDisable")
        }
    }
}


// 배차가능 요일 초기화
function dispatchWeekDelete() {
    const ableWeek = document.querySelectorAll(".ableWeek")
    for (i = 0; i < ableWeek.length; i++) {
        ableWeek[i].classList.remove("ableWeek")
    }
    for (i = 7; i < 14; i++) {
        driveWeek[i].style.backgroundColor = "white"
        driveWeek[i].style.pointerEvents = "auto"
    }
}


// 배차가능 요일
function dispatchWeekCheker() {
    for (i = 0; i < 7; i++) {
        if (driveWeek[i].checked) {
            driveWeek[i + 7].classList.add("ableWeek")
        } else {
            driveWeek[i + 7].style.backgroundColor = "#E4E4E4"
            driveWeek[i + 7].style.pointerEvents = "none"
        }
    }
}