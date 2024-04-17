const dispatchLine = document.querySelectorAll(".orderListMain")
const connectMemberInput = document.querySelector(".thisRoute .connectMemberInput")
const orderOutSoursing = document.querySelectorAll(".orderOutSoursing")
const driverTd = document.querySelectorAll(".driverTd")
const removeBtn = document.querySelectorAll(".removeBtn")
const hiddenBus = document.querySelectorAll(".hiddenBus")
const scheduleTableTr = document.querySelectorAll(".scheduleTableTr")
const dispatchPaymentCheckbox = document.querySelectorAll(".dispatchPaymentCheckbox")
const connectBusInput = document.querySelector(".connectBusInput")

const thisAssignment = document.querySelector('.thisRoute')
let ADD_SELECT = true;

// 일반배차
for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", addOrderDispatch)
}


function addOrderDispatch() {
    if (!this.parentNode.classList.contains("haveSchedule")) {

        const detailDepartureDate = `${inputTextquarter[0].value} ${inputTextTwice[0].value}:${inputTextTwice[1].value}`
        const detailArrivalData = `${inputTextquarter[1].value} ${inputTextTwice[2].value}:${inputTextTwice[3].value}`


        let targetBus = this

        let busNum = ""
        let busId = ""
        let driverName = ""
        let driverId = ""

        if (params.get("id") !== null) {
            let beforeArr = []
            let afterArr = []
            let beforeRangeEnd = ""
            let beforeRangeStart = ""
            let afterRangeEnd = ""
            let afterRangeStart = ""


            //시간범위 설정
            beforeRangeEnd = `${inputTextquarter[0].value.replace(/\-/g, "")}${inputTextTwice[0].value}${inputTextTwice[1].value}`
            if (inputTextTwice[0].value >= 11) {
                beforeRangeStart = `${inputTextquarter[0].value.replace(/\-/g, "")}${inputTextTwice[0].value - 1}${inputTextTwice[1].value}`
            } else {
                beforeRangeStart = `${inputTextquarter[0].value.replace(/\-/g, "")}0${inputTextTwice[0].value - 1}${inputTextTwice[1].value}`
            }
            afterRangeStart = `${inputTextquarter[1].value.replace(/\-/g, "")}${inputTextTwice[2].value}${inputTextTwice[3].value}`
            if (inputTextTwice[2].value >= 10) {
                afterRangeEnd = `${inputTextquarter[1].value.replace(/\-/g, "")}${inputTextTwice[2].value + 1}${inputTextTwice[3].value}`
            } else {
                afterRangeEnd = `${inputTextquarter[1].value.replace(/\-/g, "")}${(inputTextTwice[2].value + 1).substr(1, 2)}${inputTextTwice[3].value}`
            }


            //시간범위에 들어가는 데이터 추출
            if (inputTextquarter[0].value == inputTextquarter[1].value) {
                for (i = 0; i < data.length; i++) {
                    if (data[i].arrival_date.replace(/[-: ]/g, "") >= beforeRangeStart && data[i].arrival_date.replace(/[-: ]/g, "") <= beforeRangeEnd) {
                        beforeArr.push(data[i])
                    }
                    if (data[i].departure_date.replace(/[-: ]/g, "") >= afterRangeStart && data[i].departure_date.replace(/[-: ]/g, "") <= afterRangeEnd) {
                        afterArr.push(data[i])
                    }
                }
            } else {
                for (i = 0; i < data.length; i++) {
                    if (data[i].arrival_date.replace(/[-: ]/g, "") >= beforeRangeStart && data[i].arrival_date.replace(/[-: ]/g, "") <= beforeRangeEnd) {
                        beforeArr.push(data[i])
                    }
                }
                for (i = 0; i < data2.length; i++) {
                    if (data2[i].departure_date.replace(/[-: ]/g, "") >= afterRangeStart && data2[i].departure_date.replace(/[-: ]/g, "") <= afterRangeEnd) {
                        afterArr.push(data2[i])
                    }
                }
            }

            //알림 출력
            for (i = 0; i < beforeArr.length; i++) {
                if (this.classList[1] == beforeArr[i].bus_id || this.classList[2] == `d${beforeArr[i].driver_id}`) {
                    if (!confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${beforeArr[i].bus_num}(${beforeArr[i].driver_name}) || ${beforeArr[i].departure_date} ~ ${beforeArr[i].arrival_date}]`)) {
                        return
                    }
                }
            }
            for (i = 0; i < afterArr.length; i++) {
                if (this.classList[1] == afterArr[i].bus_id || this.classList[2] == `d${afterArr[i].driver_id}`) {
                    if (!confirm(`운행종료 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${afterArr[i].bus_num}(${afterArr[i].driver_name}) || ${afterArr[i].departure_date} ~ ${afterArr[i].arrival_date}]`)) {
                        return
                    }
                }
            }

            let makeSelect = true
            if (USE_VEHICLE) {
                busNum = this.innerText.substr(0,4)
                busId = this.classList[1]
                if(this.innerText.length > 4) {
                    driverName = this.innerText.split("(")[1].replace(/\)/g, "")
                } else {
                    driverName = ""
                }

                if(this.classList[2] === "d") {
                    driverId = ""
                } else {
                    driverId = this.classList[2].split("d")[1]
                }

                connectBusInput.value = busNum
                document.querySelector(".connectBusId").value = busId


                for (i = 0; i < dataList.length; i++) {
                    departureDate = dataList[i].departure_date
                    arrivalDate = dataList[i].arrival_date
                    if (driverName == dataList[i].driver_name) {
                        if (detailArrivalData >= departureDate && detailDepartureDate <= arrivalDate) {
                            makeSelect = false
                        }
                    }
                };
            } else {
                driverName = this.innerText
                driverId = this.classList[1]
            }
            

            // 
            
            

            
            if (makeSelect) {
                connectMemberInput.innerText = ""
                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${driverId}`);
                driverOption.innerText = driverName
                connectMemberInput.appendChild(driverOption);
            }
            ADD_SELECT = true
            return
        }
    }
}




// 배차가능 기사 필터(기사-옵션)
connectMemberInput?.addEventListener("click", addDriverOption);


function addDriverOption() {
    if (ADD_SELECT) {
        // 1. 선택된 기사존재여부 -> 첫번째 옵션 저장

        let firstOption = []

        if (this.children.length !== 0) {
            for (i = 0; i < this.children.length; i++) {
                if (this.children[i].selected) {
                    firstOption.push(this.children[i].value)
                    firstOption.push(this.children[i].innerText)
                }
            }
        } else {
            firstOption.push("")
            firstOption.push("")
        }
        

        // 2. this 옵션 삭제

        this.innerText = ""

        // 3. 배차불가 기사 추출 -> 기간 필터링

        let periodFilter = []

        for (i = 0; i < dataList.length; i++) {
            if (dataList[i].outSoursing !== "y") {
                dataStartTime = dataList[i].departure_date.substr(0, 10).replace(/\-/g, "") + dataList[i].departure_date.substr(11, 5).replace(/\:/g, "")
                dataEndTime = dataList[i].arrival_date.substr(0, 10).replace(/\-/g, "") + dataList[i].arrival_date.substr(11, 5).replace(/\:/g, "")
            }
            CreateCompareTime()
            if (dataEndTime >= inputStartTime && dataStartTime <= inputEndTime) {
                periodFilter.push(`${dataList[i].driver_id}`)
            }
        }

        // 4. 다른 차량의 기사목록 추출 -> 배차불가 기사

        let selectedDriver = []

        for (i = 0; i < connectMemberInput.length; i++) {
            for (j = 0; j < connectMemberInput[i].children.length; j++) {
                if (connectMemberInput[i].children[j].selected) {
                    selectedDriver.push(connectMemberInput[i].children[j].value)
                }
            }
        }

        // 5. 배차가능 기사 추출 -> 기사데이터 - 3번 - 4번

        let useDriver = []

        for (i = 0; i < Object.keys(driverObj).length; i++) {
            useDriver.push(Object.keys(driverObj)[i])
        }

        for (i = 0; i < periodFilter.length; i++) {
            useDriver = useDriver.filter(current => current !== periodFilter[i])
        }

        for (i = 0; i < selectedDriver.length; i++) {
            useDriver = useDriver.filter(current => current !== selectedDriver[i])
        }

        // 5-2. 배차가능 기사 추출 -> 현재 선택기사 제거
        useDriver = useDriver.filter(current => current !== firstOption[0])

        // 6. 배차가능 배열 오브젝트로 변경

        let useDriverSort = []

        for (i = 0; i < Object.keys(driverObj).length; i++) {
            for (j = 0; j < useDriver.length; j++) {
                if (Object.keys(driverObj)[i] == useDriver[j]) {
                    let useDriveObj = {
                        name: `${Object.keys(driverObj)[i]}`,
                        driver: `${Object.values(driverObj)[i]}`
                    }
                    useDriverSort.push(useDriveObj)
                }
            }
        }

        // 7. 배차가능 오브젝트 정렬

        useDriverSort.sort(function (a, b) {
            return a.driver < b.driver ? -1 : a.driver > b.driver ? 1 : 0;
        });

        // 8. 첫번째 옵션 생성 -> 1번

        const driverOption = document.createElement('option');
        driverOption.setAttribute("value", `${firstOption[0]}`);
        driverOption.innerText = `${firstOption[1]}`
        this.appendChild(driverOption);

        // 9. 선택가능 기사 옵션 생성 -> 5번

        // this.appendChild(document.createElement('option'));
        for (i = 0; i < useDriverSort.length; i++) {
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${useDriverSort[i].name}`);
            driverOption.innerText = `${useDriverSort[i].driver}`
            this.appendChild(driverOption);
        }
        ADD_SELECT = false
    }
}

// 기사 변경시 배차간격 팝업

connectMemberInput?.addEventListener("change", rangePopup)



function rangePopup() {
    let selectOption = ""

    for (i = 0; i < this.children.length; i++) {
        if (this.children[i].selected) {
            selectOption = this.children[i].value
        }
    }

    let beforeArr = []
    let afterArr = []
    let beforeRangeEnd = ""
    let beforeRangeStart = ""
    let afterRangeEnd = ""
    let afterRangeStart = ""


    //시간범위 설정
    beforeRangeEnd = `${inputTextquarter[0].value.replace(/\-/g, "")}${inputTextTwice[0].value}${inputTextTwice[1].value}`
    if (inputTextTwice[0].value >= 11) {
        beforeRangeStart = `${inputTextquarter[0].value.replace(/\-/g, "")}${inputTextTwice[0].value - 1}${inputTextTwice[1].value}`
    } else {
        beforeRangeStart = `${inputTextquarter[0].value.replace(/\-/g, "")}0${inputTextTwice[0].value - 1}${inputTextTwice[1].value}`
    }
    afterRangeStart = `${inputTextquarter[1].value.replace(/\-/g, "")}${inputTextTwice[2].value}${inputTextTwice[3].value}`
    if (inputTextTwice[2].value >= 10) {
        afterRangeEnd = `${inputTextquarter[1].value.replace(/\-/g, "")}${inputTextTwice[2].value + 1}${inputTextTwice[3].value}`
    } else {
        afterRangeEnd = `${inputTextquarter[1].value.replace(/\-/g, "")}${(inputTextTwice[2].value + 1).substr(1, 2)}${inputTextTwice[3].value}`
    }


    //시간범위에 들어가는 데이터 추출
    if (inputTextquarter[0].value == inputTextquarter[1].value) {
        for (i = 0; i < data.length; i++) {
            if (data[i].arrival_date.replace(/[-: ]/g, "") >= beforeRangeStart && data[i].arrival_date.replace(/[-: ]/g, "") <= beforeRangeEnd) {
                beforeArr.push(data[i])
            }
            if (data[i].departure_date.replace(/[-: ]/g, "") >= afterRangeStart && data[i].departure_date.replace(/[-: ]/g, "") <= afterRangeEnd) {
                afterArr.push(data[i])
            }
        }
    } else {
        for (i = 0; i < data.length; i++) {
            if (data[i].arrival_date.replace(/[-: ]/g, "") >= beforeRangeStart && data[i].arrival_date.replace(/[-: ]/g, "") <= beforeRangeEnd) {
                beforeArr.push(data[i])
            }
        }
        for (i = 0; i < data2.length; i++) {
            if (data2[i].departure_date.replace(/[-: ]/g, "") >= afterRangeStart && data2[i].departure_date.replace(/[-: ]/g, "") <= afterRangeEnd) {
                afterArr.push(data2[i])
            }
        }
    }


    // 알림 출력
    if (beforeArr.length !== 0 || afterArr.length !== 0) {
        for (i = 0; i < beforeArr.length; i++) {
            if (selectOption == beforeArr[i].driver_id) {
                if (!confirm(`운행시작 1시간 이내에 노선이 있습니다. 배정하시겠습니까?\n[${beforeArr[i].bus_num}(${beforeArr[i].driver_name}) || ${beforeArr[i].departure_date} ~ ${beforeArr[i].arrival_date}]`)) {
                    this.innerText = ""
                    const driverOption = document.createElement('option');
                    driverOption.setAttribute("value", `${selectDriver[0]}`);
                    driverOption.innerText = selectDriver[1]
                    this.appendChild(driverOption);
                    return
                }
            } else {
                return
            }
        }
        for (i = 0; i < afterArr.length; i++) {
            if (selectOption == afterArr[i].driver_id) {
                if (!confirm(`운행종료 1시간 이내에 노선이 있습니다. 배정하시겠습니까?\n[${afterArr[i].bus_num}(${afterArr[i].driver_name}) || ${afterArr[i].departure_date} ~ ${afterArr[i].arrival_date}]`)) {
                    this.innerText = ""
                    const driverOption = document.createElement('option');
                    driverOption.setAttribute("value", `${selectDriver[0]}`);
                    driverOption.innerText = selectDriver[1]
                    this.appendChild(driverOption);
                    return
                }
            } else {
                return
            }
        }
    } else {
        return
    }


}



// 시간비교 만들기
function CreateCompareTime() {
    inputStartTime = inputTextquarter[0].value.replace(/\-/g, "") + inputTextTwice[0].value + inputTextTwice[1].value
    inputEndTime = inputTextquarter[1].value.replace(/\-/g, "") + inputTextTwice[2].value + inputTextTwice[3].value
}



const assignmentConnectSaveBtn = document.querySelector(".assignmentConnectSaveBtn")
const connectForm = document.querySelector(".connectForm")

assignmentConnectSaveBtn.addEventListener("click", assignmentConnectSave)

function assignmentConnectSave() {
    let bus = ""
    let driver = ""

    bus = USE_VEHICLE ? connectBusInput.value : ""
    driver = connectMemberInput
    if (driver == "") {
        alert("직원을 선택해 주세요")
    } else if (bus == "" && USE_VEHICLE) {
        alert("차량을 선택해 주세요")
    } else {
        connectForm.submit();
    }
}

// connect delete
const connectDeleteBtn = document.querySelector(".connectDeleteBtn")

connectDeleteBtn.addEventListener("click", deleteConnect)

function deleteConnect() {
    connectForm.action = CONNECT_DELETE_URL
    if (confirm("배차를 삭제하시겠습니까?"))
    connectForm.submit();
}