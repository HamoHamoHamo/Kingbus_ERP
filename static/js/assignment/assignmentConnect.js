const driveTimeSh = document.querySelector(".routeTime input:nth-child(1)")
const driveTimeSM = document.querySelector(".routeTime input:nth-child(2)")
const driveTimeEh = document.querySelector(".routeTime input:nth-child(3)")
const driveTimeEM = document.querySelector(".routeTime input:nth-child(4)")

for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", regularlyDispatch)
}

let busNum = ""
let busId = ""
let DriverName = ""
let DriverId = ""

function regularlyDispatch() {

    if (!this.parentNode.classList.contains("haveSchedule")) {
        const busSchedule = this.parentNode.querySelectorAll(".scheduleBar")

        let timeArr = []
        let rangeBeforeArr = []
        let rangeAfterArr = []

        for (i = 0; i < busSchedule.length; i++) {
            timeArr.push(
                {
                    start: `${busSchedule[i].title.split("|| ")[1].split("||")[0].replace(/\ /g, "").split("~")[0].replace(/\:/g, "")}`,
                    end: `${busSchedule[i].title.split("|| ")[1].split("||")[0].replace(/\ /g, "").split("~")[1].replace(/\:/g, "")}`,
                    bus: `${this.innerText.split("(")[0]}`,
                    driver: `${busSchedule[i].title.split("||")[0].replace(/\ /g, "")}`
                }
            )
        };


        inputStartTime = parseInt(`${regularlyTime[0].value}${regularlyTime[1].value}`)
        inputEndTime = parseInt(`${regularlyTime[2].value}${regularlyTime[3].value}`)
        inputStartTimeRange = parseInt(`${parseInt(regularlyTime[0].value) - 1}${regularlyTime[1].value}`)
        inputEndTimeRange = parseInt(`${parseInt(regularlyTime[2].value) + 1}${regularlyTime[3].value}`)


        for (i = 0; i < timeArr.length; i++) {
            if (timeArr[i].end < inputStartTime && timeArr[i].end >= inputStartTimeRange) {
                rangeBeforeArr.push(timeArr[i])
            } else if (timeArr[i].start > inputEndTime && timeArr[i].start <= inputEndTimeRange) {
                rangeAfterArr.push(timeArr[i])
            }
        };


        let rangeCounter = 0
        if (rangeBeforeArr.length !== 0 || rangeAfterArr.length !== 0) {
            for (i = 0; i < rangeBeforeArr.length; i++) {
                if (confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${rangeBeforeArr[i].bus}(${rangeBeforeArr[i].driver}) || ${rangeBeforeArr[i].start.substr(0, 2)}:${rangeBeforeArr[i].start.substr(2, 2)} ~ ${rangeBeforeArr[i].end.substr(0, 2)}:${rangeBeforeArr[i].end.substr(2, 2)}]`)) {
                    rangeCounter = rangeCounter + 1
                }
            };
            for (i = 0; i < rangeAfterArr.length; i++) {
                if (confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${rangeAfterArr[i].bus}(${rangeAfterArr[i].driver}) || ${rangeAfterArr[i].start.substr(0, 2)}:${rangeAfterArr[i].start.substr(2, 2)} ~ ${rangeAfterArr[i].end.substr(0, 2)}:${rangeAfterArr[i].end.substr(2, 2)}]`)) {
                    rangeCounter = rangeCounter + 1
                }
            };
        }

        if (rangeCounter == rangeBeforeArr.length + rangeAfterArr.length) {
            const driverSelect = document.querySelector(".driverSelect")
            let makeSelect = true
            if (USE_VEHICLE) {
                const businput = document.querySelector(".selectRoute input[type=text]")
                const busIdHidden = document.querySelector(".RouteList input[name=bus]")
    
                busNum = this.innerText.split("(")[0]
                busId = this.classList[1]
                if(this.innerText.length > 4){
                    DriverName = this.innerText.split("(")[1].replace(/\)/g, "")
                }else{
                    DriverName = ""
                }
                if(this.classList[2] === "d"){
                    DriverId = ""
                }else{
                    DriverId = this.classList[2].split("d")[1]
                }
    
                businput.value = busNum;
                busIdHidden.value = busId;
    
    
                let departureInput = `${driveTimeSh.value}` + `${driveTimeSM.value}`
                let arrivalInput = `${driveTimeEh.value}` + `${driveTimeEM.value}`
                let arrivalDate = ""
                let departureDate = ""
    
                for (i = 0; i < dataList.length; i++) {
                    departureDate = dataList[i].departure_date.split(" ")[1].replace(/\:/g, "")
                    arrivalDate = dataList[i].arrival_date.split(" ")[1].replace(/\:/g, "")
                    if(this.innerText.length > 4){
                        if (this.innerText.split("(")[1].replace(/\)/g, "") == dataList[i].driver.name) {
                            if (arrivalInput >= departureDate && departureInput <= arrivalDate) {
                                return makeSelect = false
                            }
                        }
                    }
                };
    
            } else {
                DriverName = this.innerText
                DriverId = this.classList[1]
            }
            if (makeSelect) {
                driverSelect.innerText = ""
                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${DriverId}`);
                driverOption.innerText = DriverName
                driverSelect.appendChild(driverOption);
            }
        }
    }
}

const assignmentConnectSaveBtn = document.querySelector(".assignmentConnectSaveBtn")

assignmentConnectSaveBtn.addEventListener("click", assignmentConnectSave)

function assignmentConnectSave() {
    let bus = ""
    let driver = ""
    for (i = 0; i < RouteListHBodyTr.length; i++) {
        if (RouteListHBodyTr[i].children[0].children[0].checked) {
            bus = USE_VEHICLE ? RouteListHBodyTr[i].children[4].children[1].value : ""
            driver = RouteListHBodyTr[i].children[5].children[0].value
        }
    };
    if (driver == "") {
        alert("직원을 선택해 주세요")
    } else if (bus == "" && USE_VEHICLE) {
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