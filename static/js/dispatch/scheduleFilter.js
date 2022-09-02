const scheduleRadio = document.querySelectorAll(".scheduleRadio")
const scheduleLabel = document.querySelectorAll(".scheduleHeaderFilterBox label")
const routeTimeInput = document.querySelectorAll(".quarterBox input")




let scheduleDay = ""
let inputStartTime = routeTimeInput[0].value + routeTimeInput[1].value
let inputEndTime = routeTimeInput[2].value + routeTimeInput[3].value
let dataStartTime = ""
let dataEndTime = ""
let scheduleBus = []


let dataTimeStart = ""
let dataTimeEnd = ""


for (i = 0; i < scheduleRadio.length; i++) {
    scheduleRadio[i].addEventListener("change", radioDateChange)
}

function radioDateChange() {
    resetSchedule()
    getChekcedDate()
    drawSchdule()
    DispatcBusFiilter()
}




window.onload = function regularly_route() {
    loadData()
    ableFixedDispatch()
    getChekcedDate()
    drawSchdule()
    DispatcBusFiilter()
}







// 스케줄 그리기
function drawSchdule() {


    for (i = 0; i < data.length; i++) {

        if (data[i].week == scheduleDay) {

            for (j = 0; j < driverTd.length; j++) {

                if (data[i].bus_id == driverTd[j].classList[1]) {

                    const startWork = document.createElement('div');

                    // 기사 동일여부
                    if (data[i].driver_id !== parseInt(driverTd[j].classList[2].split("d")[1])) {

                        // 타입구분
                        if (data[i].work_type == "출근") {
                            startWork.setAttribute("class", "regularlyLineStart scheduleBar otherDriver");
                        } else {
                            startWork.setAttribute("class", "regularlyLineEnd scheduleBar otherDriver");
                        }

                    } else {

                        // 타입구분
                        if (data[i].work_type == "출근") {
                            startWork.setAttribute("class", "regularlyLineStart scheduleBar");
                        } else {
                            startWork.setAttribute("class", "regularlyLineEnd scheduleBar");
                        }

                    }

                    // 스타일 부여
                    dataTimeStart = parseInt(data[i].departure_time.split(":")[0] * 60) + parseInt(data[i].departure_time.split(":")[1])
                    dataTimeEnd = parseInt(data[i].arrival_time.split(":")[0] * 60) + parseInt(data[i].arrival_time.split(":")[1])

                    startWork.setAttribute("style", `left: ${dataTimeStart * 0.074}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.074}rem;`);

                    // title 부여

                    startWork.setAttribute("title", `${data[i].driver_name} || ${data[i].departure}▶${data[i].arrival}`);

                    // 스케줄 생성
                    driverTd[j].parentNode.appendChild(startWork);
                }
            }
        }
    }
}







// 배차불가 차량 필터
function DispatcBusFiilter() {

    scheduleBus = []

    // data요일 필터링
    for (i = 0; i < data.length; i++) {
        if (data[i].week == scheduleDay) {

            dataStartTime = data[i].departure_time.replace(/\:/g, "")
            dataEndTime = data[i].arrival_time.replace(/\:/g, "")

            // data기간 필터링
            if (dataEndTime >= inputStartTime && inputEndTime >= dataStartTime) {
                scheduleBus.push(data[i].bus_id)
            }
        }
    }

    // 배차불가 클래스 부여
    for (i = 0; i < scheduleBus.length; i++) {
        for (j = 0; j < driverTd.length; j++) {
            if (driverTd[j].classList[1] == scheduleBus[i]) {
                driverTd[j].parentNode.classList.add("haveSchedule")
            }
        }
    }
}






// 선택된 요일 구하기
function getChekcedDate() {

    // 선택요일 구하기
    for (i = 0; i < scheduleRadio.length; i++) {
        if (scheduleRadio[i].checked) {
            scheduleDay = scheduleLabel[i].innerText;
        }
    }
}





// 스케줄 초기화
function resetSchedule() {
    const scheduleBar = document.querySelectorAll(".scheduleBar")
    for (i = 0; i < scheduleBar.length; i++) {
        scheduleBar[i].remove()
    }
    for (i = 0; i < driverTd.length; i++) {
        if (driverTd[i].parentNode.classList.contains("haveSchedule")) {
            driverTd[i].parentNode.classList.remove("haveSchedule")
        }
    }
}