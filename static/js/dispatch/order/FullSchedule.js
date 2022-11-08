const sheduleLine = document.querySelectorAll(".scheduleTableTr")
const scheduleRadio = document.querySelectorAll(".scheduleRadio")
const scheduleLabel = document.querySelectorAll(".scheduleHeaderFilterBox label")
const regularlyTime = document.querySelectorAll(".routeTime .inputText")




let dataStartDate = ""
let dataEndDate = ""
let dataStartTime = ""
let dataEndTime = ""
let scheduleBus = []





// 스케줄 그리기
function drawSchdule() {

    for (i = 0; i < dataList.length; i++) {

        if (dataList[i].work_type === "일반" || dataList[i].departure_date.split(" ")[0] === inputTextquarter[0].value) {

            for (j = 0; j < driverTd.length; j++) {

                if (dataList[i].bus_id == driverTd[j].classList[1]) {

                    const startWork = document.createElement('div');

                    // 기사 동일여부
                    if (dataList[i].driver_id !== parseInt(driverTd[j].classList[2].split("d")[1])) {

                        // 타입구분
                        if (dataList[i].work_type == "출근") {
                            startWork.setAttribute("class", "regularlyLineStart scheduleBar otherDriver");
                        } else if (dataList[i].work_type == "퇴근") {
                            startWork.setAttribute("class", "regularlyLineEnd scheduleBar otherDriver");
                        } else {
                            startWork.setAttribute("class", "orderLine scheduleBar otherDriver");
                        }

                    } else {

                        // 타입구분
                        if (dataList[i].work_type == "출근") {
                            startWork.setAttribute("class", "regularlyLineStart scheduleBar");
                        } else if (dataList[i].work_type == "퇴근") {
                            startWork.setAttribute("class", "regularlyLineEnd scheduleBar");
                        } else {
                            startWork.setAttribute("class", "orderLine scheduleBar");
                        }

                    }

                    dataStartDate = dataList[i].departure_date.split(" ")[0]
                    dataEndDate = dataList[i].arrival_date.split(" ")[0]

                    // 스타일 부여
                    dataTimeStart = parseInt(dataList[i].departure_date.substr(11, 5).split(":")[0] * 60) + parseInt(dataList[i].departure_date.substr(11, 5).split(":")[1])
                    dataTimeEnd = parseInt(dataList[i].arrival_date.substr(11, 5).split(":")[0] * 60) + parseInt(dataList[i].arrival_date.substr(11, 5).split(":")[1])

                    // data기간 필터링
                    if(params.has("id")){
                        if (dataStartDate == dataEndDate) {
                            startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                        } else {
                            startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                        }
                    }else{
                        if (dataStartDate == searchDate[0].value && dataEndDate !== searchDate[1].value) {
                            startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                        } else if (dataEndDate == searchDate[0].value && dataStartDate !== searchDate[1].value) {
                            startWork.setAttribute("style", `left: 0rem; width: ${dataTimeEnd * 0.0161}rem;`);
                        } else if (dataStartDate == dataEndDate) {
                            startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                        } else {
                            startWork.setAttribute("style", `left: 0rem; width: 23.184rem;`);
                        }
                    }

                    // title 부여
                    if(dataStartDate == dataEndDate){
                        startWork.setAttribute("title", `${dataList[i].driver_name} || ${dataList[i].departure_date.split(" ")[1]}~${dataList[i].arrival_date.split(" ")[1]} || ${dataList[i].departure}▶${dataList[i].arrival}`);   
                    }else{
                        startWork.setAttribute("title", `${dataList[i].driver_name} || ${dataList[i].departure_date.split(" ")[0]} [${dataList[i].departure_date.split(" ")[1]}]~${dataList[i].arrival_date.split(" ")[0]} [${dataList[i].arrival_date.split(" ")[1]}] || ${dataList[i].departure}▶${dataList[i].arrival}`);
                    }
                    // 스케줄 생성
                    driverTd[j].parentNode.appendChild(startWork);
                }
            }
        }
    }
}






// 배차불가 차량 필터(일반배차)
function DispatcBusFilter() {

    scheduleBus = []

    for (i = 0; i < dataList.length; i++) {

        dataStartTime = dataList[i].departure_date.substr(0, 10).replace(/\-/g, "") + dataList[i].departure_date.substr(11, 5).replace(/\:/g, "")
        dataEndTime = dataList[i].arrival_date.substr(0, 10).replace(/\-/g, "") + dataList[i].arrival_date.substr(11, 5).replace(/\:/g, "")


        CreateCompareTime()

        // data기간 필터링
        if (dataEndTime >= inputStartTime && dataStartTime <= inputEndTime) {
            scheduleBus.push(dataList[i].bus_id)
        }
    }


    // 배차불가 클래스 부여
    if (inputStartTime !== "" && inputEndTime !== "") {
        for (i = 0; i < scheduleBus.length; i++) {
            for (j = 0; j < driverTd.length; j++) {
                if (driverTd[j].classList[1] == scheduleBus[i]) {
                    driverTd[j].parentNode.classList.add("haveSchedule")
                }
            }
        }
    }
}





// 기사와 차량이 고정기사와 맞지 않을때
function notPairFilter() {
    const otherDriver = document.querySelectorAll(".otherDriver")
    for (i = 0; i < otherDriver.length; i++) {
        if (otherDriver[i].parentNode.classList.contains("haveSchedule")) {
            for (j = 0; j < driverTd.length; j++) {
                if (driverTd[j].innerText.split("(")[1].replace(/\)/g, "") == otherDriver[i].title.split(" ||")[0]) {
                    driverTd[j].parentNode.classList.add("haveSchedule")
                }
            }
        }
    }
}