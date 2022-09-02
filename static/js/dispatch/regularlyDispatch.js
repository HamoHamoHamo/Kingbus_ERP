const routeList = document.querySelectorAll(".listTable tbody tr")
const routeListBus = document.querySelectorAll(".listTable tbody td:nth-child(3)")
const orderDriver = document.querySelectorAll(".orderDriver")
const orderSpareDriver = document.querySelectorAll(".orderSpareDriver")
const scheduleTableTr = document.querySelectorAll(".scheduleTableTr")




// 배차 가능 노선 표시
function dispatchCheck() {
    if (window.location.search.substr(0, 3) == "?id") {
        for (i = 0; i < routeList.length; i++) {
            if (routeList[i].classList[0] == window.location.search.split("=")[1].split("&")[0]) {
                routeList[i].classList.add("checkBus")
                routeList[i].children[2].style.backgroundColor = "#0069D9"
                routeList[i].children[2].style.color = "white"
                routeList[i].children[3].style.backgroundColor = "#0069D9"
                routeList[i].children[4].style.backgroundColor = "#0069D9"
            }
        }
    }
}




// 배차
for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", addDDispatch)
}

function addDDispatch() {
    let busNum = ""
    let busId = ""
    let DriverName = ""
    let DriverId = ""

    // 정보추출
    if (!this.parentNode.classList.contains("haveSchedule")) {
        busNum = this.innerText.substr(0, 4)
        busId = this.classList[1]
        DriverName = this.innerText.split("(")[1].replace(/\)/g, "")
        DriverId = this.classList[2].split("d")[1]

        // 배차생성
        for (i = 0; i < routeList.length; i++) {
            if (routeList[i].classList.contains(`${window.location.search.split("id=")[1].split("&group")[0]}`)) {
                routeList[i].children[2].innerText = busNum
                routeList[i].children[9].value = busId

                orderDriver[i].children[0].remove()

                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${DriverId}`);
                driverOption.innerText = DriverName
                orderDriver[i].appendChild(driverOption);
            }
        }
    }
    useDriver()
}




// 운전원, 용역 보이기
function useDriver() {
    for (i = 0; i < routeList.length; i++) {
        if (routeList[i].classList.contains(`${window.location.search.split("id=")[1].split("&group")[0]}`) && routeList[i].children[2].innerText !== "") {
            orderDriver[i].style.display = "block"
            orderSpareDriver[i].style.display = "block"
        }
    }
}




// 운전원, 용역 변경시 새로고침 막기
for (i = 0; i < orderDriver.length; i++) {
    orderDriver[i].addEventListener("click", stopLink)
    orderSpareDriver[i].addEventListener("click", stopLink)
}

function stopLink(e) {
    e.stopPropagation()
}






// 배차가능 기사 옵션 추가
for(i=0; i<orderDriver.length; i++){
    orderDriver[i].addEventListener("click", addDriverOption)
}

function addDriverOption() {


    if (this.children.length == 1) {

        scheduleBus = []

        for (i = 0; i < data.length; i++) {

            dataStartDate = data[i].departure_date.substr(0, 10)
            dataEndDate = data[i].arrival_date.substr(0, 10)
            dataStartTime = data[i].departure_date.substr(11, 5).replace(/\:/g, "")
            dataEndTime = data[i].arrival_date.substr(11, 5).replace(/\:/g, "")
    
            // data기간 필터링
            if (dataStartDate == searchDate.value && dataEndDate !== searchDate.value) {
                if (inputEndTime >= dataStartTime) {
                    scheduleBus.push(data[i].driver_id)
                }
            } else if (dataEndDate == searchDate.value && dataStartDate !== searchDate.value) {
                if (dataEndTime >= inputStartTime) {
                    scheduleBus.push(data[i].driver_id)
                }
            } else if (dataStartDate == dataEndDate) {
                if (dataEndTime >= inputStartTime && inputEndTime >= dataStartTime) {
                    scheduleBus.push(data[i].driver_id)
                }
            } else {
                scheduleBus.push(data[i].driver_id)
            }
        }

        // 배차불가 차량 필터링
        let optionDriver = Object.keys(driverObj)
        for (i = 0; i < scheduleBus.length; i++) {
            optionDriver = optionDriver.filter((current) => current !== `${scheduleBus[i]}`)
        }

        let optionDriverKo = []
        for (i = 0; i < optionDriver.length; i++) {
            optionDriverKo.push(driverObj[optionDriver[i]])
        }

        function ascending(a, b) { return (a < b) ? -1 : (a == b) ? 0 : 1; }
        optionDriverKo.sort(ascending);

        let optionDriverSort = []
        for (i = 0; i < optionDriverKo.length; i++) {
            for (j = 0; j < optionDriver.length; j++) {
                if (driverObj[optionDriver[j]] == optionDriverKo[i]) {
                    optionDriverSort.push(optionDriver[j])
                }
            }
        }


        // 배차가능 차량 옵션 추가
        for (i = 0; i < optionDriverKo.length; i++) {
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${optionDriverSort[i]}`);
            driverOption.innerText = optionDriverKo[i]
            this.appendChild(driverOption);
        }
    }
}