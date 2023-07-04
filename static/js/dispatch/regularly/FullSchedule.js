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

    for (i = 0; i < data.length; i++) {

        for (j = 0; j < driverTd.length; j++) {

            if (data[i].bus_id == driverTd[j].classList[1]) {

                const startWork = document.createElement('div');

                // 기사 동일여부
                if (data[i].driver_id !== parseInt(driverTd[j].classList[2].split("d")[1])) {

                    // 타입구분
                    if (data[i].work_type == "출근") {
                        startWork.setAttribute("class", "regularlyLineStart scheduleBar otherDriver");
                    } else if (data[i].work_type == "퇴근") {
                        startWork.setAttribute("class", "regularlyLineEnd scheduleBar otherDriver");
                    } else {
                        startWork.setAttribute("class", "orderLine scheduleBar otherDriver");
                    }

                } else {

                    // 타입구분
                    if (data[i].work_type == "출근") {
                        startWork.setAttribute("class", "regularlyLineStart scheduleBar");
                    } else if (data[i].work_type == "퇴근") {
                        startWork.setAttribute("class", "regularlyLineEnd scheduleBar");
                    } else {
                        startWork.setAttribute("class", "orderLine scheduleBar");
                    }

                }

                dataStartDate = data[i].departure_date.split(" ")[0]
                dataEndDate = data[i].arrival_date.split(" ")[0]


                // 스타일 부여
                dataTimeStart = parseInt(data[i].departure_date.substr(11, 5).split(":")[0] * 60) + parseInt(data[i].departure_date.substr(11, 5).split(":")[1])
                dataTimeEnd = parseInt(data[i].arrival_date.substr(11, 5).split(":")[0] * 60) + parseInt(data[i].arrival_date.substr(11, 5).split(":")[1])

                // data기간 필터링
                if (dataStartDate == searchDate.value && dataEndDate !== searchDate.value) {
                    startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: calc(100%  - (100% - 23.184rem) - ${dataTimeStart * 0.0161}rem);`);
                } else if (dataEndDate == searchDate.value && dataStartDate !== searchDate.value) {
                    startWork.setAttribute("style", `left: 0rem; width: ${dataTimeEnd * 0.0161}rem;`);
                } else if (dataStartDate == dataEndDate) {
                    startWork.setAttribute("style", `left: ${dataTimeStart * 0.0161}rem; width: ${(dataTimeEnd - dataTimeStart) * 0.0161}rem;`);
                } else {
                    startWork.setAttribute("style", `left: 0rem; width: 23.184rem;`);
                }

                // title 부여

                startWork.setAttribute("title", `${data[i].driver_name} || ${data[i].departure_date.split(" ")[1]}~${data[i].arrival_date.split(" ")[1]} || ${data[i].departure}▶${data[i].arrival}`);

                //// 배차확인 값 따라 backgroundColor 변경
                //if (data[i].connect_check == '')
                //{
                //    startWork.style.border = '1px solid black';
                //    startWork.style.backgroundColor = 'gray';
                //}
                //else if (data[i].connect_check == '0')
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

    inputStartTime = parseInt(`${regularlyTime[0].value}${regularlyTime[1].value}`)
    inputEndTime = parseInt(`${regularlyTime[2].value}${regularlyTime[3].value}`)

    for (i = 0; i < data.length; i++) {

        dataStartTime = parseInt(data[i].departure_date.split(" ")[1].replace(/\:/g, ""))
        dataEndTime = parseInt(data[i].arrival_date.split(" ")[1].replace(/\:/g, ""))


        // data기간 필터링
        if (inputEndTime >= dataStartTime && inputStartTime <= dataEndTime) {
            scheduleBus.push(data[i].bus_id)
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