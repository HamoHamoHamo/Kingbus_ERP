const routeList = document.querySelectorAll(".listTable tbody tr")
const routeListBus = document.querySelectorAll(".listTable tbody td:nth-child(3)")
const orderDriver = document.querySelectorAll(".orderDriver")
const orderSpareDriver = document.querySelectorAll(".orderSpareDriver")
const scheduleTableTr = document.querySelectorAll(".scheduleTableTr")
const driverTd = document.querySelectorAll(".driverTd")
const routeTimeInput = document.querySelectorAll(".quarterBox input")





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





// 시간비교 만들기
function CreateCompareTime() {
    inputStartTime = searchDate.value.replace(/\-/g, "") + routeTimeInput[0].value + routeTimeInput[1].value
    inputEndTime = searchDate.value.replace(/\-/g, "") + routeTimeInput[2].value + routeTimeInput[3].value

}