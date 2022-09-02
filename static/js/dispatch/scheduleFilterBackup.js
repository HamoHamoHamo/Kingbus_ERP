const sheduleLine = document.querySelectorAll(".scheduleTableTr")
const scheduleRadio = document.querySelectorAll(".scheduleRadio")
const scheduleLabel = document.querySelectorAll(".scheduleHeaderFilterBox label")
const routeTimeInput = document.querySelectorAll(".quarterBox input")
const driverTd = document.querySelectorAll(".driverTd")

// 노선 운행시간
let routeTimeStart = 0;
let routeTimeEnd = 0;

function getRouteTime() {
    routeTimeStart = parseInt(routeTimeInput[0].value * 60) + parseInt(routeTimeInput[1].value)
    routeTimeEnd = parseInt(routeTimeInput[2].value * 60) + parseInt(routeTimeInput[3].value)
}


window.onload = function () {
    dispatchCheck()
    inputToDay()
    useDriver()
    getRouteTime()
    drawSchdule()
    BothDriverDispatch()
    ableToDispatch()
    // loadData()
}


// 스케줄 메인
function drawSchdule() {
    // 차량 키 배열
    let dataKey = Object.keys(data)

    if (window.location.search !== "") {

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
                    let startDay = parseInt(weekObj[weekKey[1]].substr(0, 10).replace(/\-/g, ""))
                    let endDay = parseInt(weekObj[weekKey[2]].substr(0, 10).replace(/\-/g, ""))
                    let StartH = parseInt(weekObj[weekKey[1]].split(" ")[1].substr(0, 2))
                    let EndH = parseInt(weekObj[weekKey[2]].split(" ")[1].substr(0, 2))
                    let StartM = parseInt(weekObj[weekKey[1]].split(" ")[1].substr(3, 2))
                    let EndM = parseInt(weekObj[weekKey[2]].split(" ")[1].substr(3, 2))
                    let startPoint = StartH * 60 + StartM
                    let endPoint = EndH * 60 + EndM
                    let scheduleWidth = (EndH * 60 + EndM) - (StartH * 60 + StartM)
                    //날짜가 다른경우 출발일 시간 = 전체 - 시작시간
                    //날짜가 다른경우 도착일 시간 = 도착시간


                    //스케줄바 생성

                    const startWork = document.createElement('div');

                    if (weekObj[weekKey[0]] == "출근") {
                        startWork.setAttribute("class", "regularlyLineStart scheduleBar");
                    }
                    else if (weekObj[weekKey[0]] == "퇴근") {
                        startWork.setAttribute("class", "regularlyLineEnd scheduleBar");
                    } else {
                        startWork.setAttribute("class", "orderLine scheduleBar");
                    }

                    startWork.setAttribute("title", `${driverObj[driverKey[j]]} || ${weekObj[weekKey[3]]}▶${weekObj[weekKey[4]]}`);
                    for (l = 0; l < sheduleLine.length; l++) {
                        if (sheduleLine[l].children[7].classList[1] == dataKey[i]) {
                            console.log(driverObj[driverKey[j]])
                            console.log(driverObj[driverKey[j]])
                            if (driverObj[driverKey[j]] == driverObj[sheduleLine[l].children[7].classList[2]]) {
                                if (startDay == endDay) {
                                    startWork.setAttribute("style", `left: ${startPoint * 0.175}rem; width: ${scheduleWidth * 0.175}rem;`);
                                }
                            } else {
                                if (startDay == parseInt(searchDate.value.replace(/\-/g, ""))) {
                                    startWork.setAttribute("style", `left: ${startPoint * 0.175}rem; width: calc(100% - ${startPoint * 0.175})rem;`);
                                } else if (endDay == parseInt(searchDate.value.replace(/\-/g, ""))) {
                                    startWork.setAttribute("style", `left: 0rem; width: ${endPoint * 0.175}rem;`);
                                } else {
                                    startWork.setAttribute("style", `left:0rem; width: 100%;`);
                                }
                            }
                        } else {
                            startWork.setAttribute("style", `left: ${startPoint * 0.175}rem; width: ${scheduleWidth * 0.175}rem; border: 0.3rem solid #FF9900; box-sizing: border-box`);
                            startWork.classList.add("bothDriver")
                        }
                        sheduleLine[l].appendChild(startWork);
                    }
                    if (endPoint >= routeTimeStart && startPoint <= routeTimeEnd) {
                        for (l = 0; l < sheduleLine.length; l++) {
                            if (sheduleLine[l].children[7].classList[1] == dataKey[i]) {
                                sheduleLine[l].children[7].classList.add("haveSchedule")
                            }
                        }
                    }
                }
            }
        }
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


// 기사변경 배차여부
function BothDriverDispatch() {
    const scheduleBar = document.querySelectorAll(".scheduleBar")

    let bothDriverDispatch = ""
    let bothDriverWidth = ""
    let bothDriverStart = ""
    for (i = 0; i < scheduleBar.length; i++) {
        if (scheduleBar[i].classList.contains("bothDriver")) {
            bothDriverDispatch = scheduleBar[i].title.split("|")[0].replace(/\ /g, "")
            bothDriverWidth = parseInt(scheduleBar[i].style.width.split("r")[0]) / 0.074
            bothDriverStart = parseInt(scheduleBar[i].style.left.split("r")[0]) / 0.074
        }
    }
    for (i = 0; i < sheduleLine.length; i++) {
        if (sheduleLine[i].children[7].innerText.split("(")[1].replace(/\)/g, "") == bothDriverDispatch) {
            if (bothDriverStart <= routeTimeStart + routeTimeEnd || bothDriverWidth + bothDriverStart >= routeTimeStart) {
                sheduleLine[i].children[7].classList.add("haveSchedule")
            }
        }
    }
}