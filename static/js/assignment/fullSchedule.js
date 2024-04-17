const sheduleLine = document.querySelectorAll(".scheduleTableTr")
const scheduleRadio = document.querySelectorAll(".scheduleRadio")
const scheduleLabel = document.querySelectorAll(".scheduleHeaderFilterBox label")
const regularlyTime = document.querySelectorAll(".routeTime .inputText")

let dataStartDate = ""
let dataEndDate = ""
let dataStartTime = ""
let dataEndTime = ""
let scheduleBus = []

const thisSearchDate = document.querySelectorAll(".searchDate")

// 스케줄 그리기
function drawSchdule() {    
    const thisDataList = CURRENT_PAGE == 'temporary_assignment' && params.has("id") ? data : dataList

    for (i = 0; i < thisDataList.length; i++) {

        for (j = 0; j < driverTd.length; j++) {

            if ((!USE_VEHICLE && thisDataList[i].driver_id == driverTd[j].classList[1]) || (USE_VEHICLE && thisDataList[i].bus_id == driverTd[j].classList[1])) {
                console.log("D ", thisDataList[i], driverTd[j])
                const startWork = document.createElement('div');
                
                // 타입구분
                if (thisDataList[i].work_type == "출근") {
                    startWork.setAttribute("class", "regularlyLineStart scheduleBar");
                } else if (thisDataList[i].work_type == "퇴근") {
                    startWork.setAttribute("class", "regularlyLineEnd scheduleBar");
                } else if (thisDataList[i].work_type == "일반") {
                    startWork.setAttribute("class", "orderLine scheduleBar");
                } else if (thisDataList[i].work_type == "고정업무") {
                    startWork.setAttribute("class", "assignmentLine scheduleBar");
                } else if (thisDataList[i].work_type == "일반업무") {
                    startWork.setAttribute("class", "temporaryAssignmentLine scheduleBar");
                }

                // 기사 동일여부
                if (USE_VEHICLE && thisDataList[i].driver_id !== parseInt(driverTd[j].classList[2].split("d")[1])) {
                    startWork.className += " otherDriver"
                }

                dataStartDate = thisDataList[i].departure_date.split(" ")[0]
                dataEndDate = thisDataList[i].arrival_date.split(" ")[0]

                // 스타일 부여
                dataTimeStart = parseInt(thisDataList[i].departure_date.substr(11, 5).split(":")[0] * 60) + parseInt(thisDataList[i].departure_date.substr(11, 5).split(":")[1])
                dataTimeEnd = parseInt(thisDataList[i].arrival_date.substr(11, 5).split(":")[0] * 60) + parseInt(thisDataList[i].arrival_date.substr(11, 5).split(":")[1])

                // data기간 필터링

                // 일반업무
                if (thisSearchDate[1] && params.has("id")) {
                    if (dataStartDate == dataEndDate) {
                        startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                    } else {
                        startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                    }
                }
                else {
                    if (dataStartDate == thisSearchDate[0].value && dataEndDate !== thisSearchDate[0].value) {
                        startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                    } else if (dataEndDate == thisSearchDate[0].value && dataStartDate !== thisSearchDate[0].value) {
                        startWork.setAttribute("style", `left: 0rem; width: ${dataTimeEnd * 0.0161}rem;`);
                    } else if (dataStartDate == thisSearchDate[0].value && dataEndDate == thisSearchDate[0].value) {
                        startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                    } else {
                        startWork.setAttribute("style", `left: 0rem; width: 23.184rem;`);
                    }
                }
                // }
                // else {
                //     if (dataStartDate == thisSearchDate.value && dataEndDate !== thisSearchDate.value) {
                //         startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                //     } else if (dataEndDate != dataStartDate) {
                //         startWork.setAttribute("style", `left: 0rem; width: ${dataTimeEnd * 0.0161}rem;`);
                //     } else if (dataStartDate == dataEndDate) {
                //         startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                //     } else {
                //         startWork.setAttribute("style", `left: 0rem; width: 23.184rem;`);
                //     }
                // }

                // title 부여                
                if (thisDataList[i].work_type == '고정업무' || thisDataList[i].work_type == '일반업무') {
                    if (dataStartDate == dataEndDate) {
                        startWork.setAttribute("title", `${thisDataList[i].driver_name} || ${thisDataList[i].departure_date.split(" ")[1]}~${thisDataList[i].arrival_date.split(" ")[1]} || ${thisDataList[i].assignment}`);
                    } else {
                        startWork.setAttribute("title", `${thisDataList[i].driver_name} || ${thisDataList[i].departure_date.split(" ")[0]} [${thisDataList[i].departure_date.split(" ")[1]}]~${thisDataList[i].arrival_date.split(" ")[0]} [${thisDataList[i].arrival_date.split(" ")[1]}] || ${thisDataList[i].assignment}`);
                    }
                } else if (dataStartDate == dataEndDate) {
                    startWork.setAttribute("title", `${thisDataList[i].driver_name} || ${thisDataList[i].departure_date.split(" ")[1]}~${thisDataList[i].arrival_date.split(" ")[1]} || ${thisDataList[i].departure.split("@")[0]}▶${thisDataList[i].arrival.split("@")[0]}`);
                } else {
                    startWork.setAttribute("title", `${thisDataList[i].driver_name} || ${thisDataList[i].departure_date.split(" ")[0]} [${thisDataList[i].departure_date.split(" ")[1]}]~${thisDataList[i].arrival_date.split(" ")[0]} [${thisDataList[i].arrival_date.split(" ")[1]}] || ${thisDataList[i].departure.split("@")[0]}▶${thisDataList[i].arrival.split("@")[0]}`);
                }

                //// 배차확인 값 따라 backgroundColor 변경
                //if (thisDataList[i].connect_check == '')
                //{
                //    startWork.style.border = '1px solid black';
                //    startWork.style.backgroundColor = 'gray';
                //}
                //else if (thisDataList[i].connect_check == '0')
                //{
                //    startWork.style.border = '1px solid black';
                //    startWork.style.backgroundColor = 'red';
                //}
                // 스케줄 생성
                driverTd[j].parentNode.appendChild(startWork);
            }
        }
    }
}



// 배차불가 차량 필터(출퇴근배차)
function DispatcBusFilterRegularly() {

    scheduleBus = []

    inputStartDate = `${URL_DATE} ${regularlyTime[0].value}:${regularlyTime[1].value}`
    inputEndDate = `${URL_DATE} ${regularlyTime[2].value}:${regularlyTime[3].value}`

    for (i = 0; i < dataList.length; i++) {

        startDate = dataList[i].departure_date
        endDate = dataList[i].arrival_date

        // data기간 필터링
        if (inputEndDate >= startDate && inputStartDate <= endDate) {
            if (USE_VEHICLE) {
                scheduleBus.push(dataList[i].bus_id)
            } else {
                scheduleBus.push(dataList[i].driver_id)
            }
        }

    }

    // 배차불가 클래스 부여
    if (inputStartDate !== "" && inputEndDate !== "") {
        for (i = 0; i < scheduleBus.length; i++) {
            for (j = 0; j < driverTd.length; j++) {
                if (driverTd[j].classList[1] == scheduleBus[i]) {
                    driverTd[j].parentNode.classList.add("haveSchedule")
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
            if (USE_VEHICLE) {
                scheduleBus.push(dataList[i].bus_id)
            } else {
                scheduleBus.push(dataList[i].driver_id)
            }


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
// function notPairFilter() {
//     const otherDriver = document.querySelectorAll(".otherDriver")
//     for (i = 0; i < otherDriver.length; i++) {
//         if (otherDriver[i].parentNode.classList.contains("haveSchedule")) {
//             for (j = 0; j < driverTd.length; j++) {
//                 if (driverTd[j].innerText.split("(")[1].replace(/\)/g, "") == otherDriver[i].title.split(" ||")[0]) {
//                     driverTd[j].parentNode.classList.add("haveSchedule")
//                 }
//             }
//         }
//     }
// }