const dispatchLine = document.querySelectorAll(".dispatcTable")
const orderDriver = document.querySelectorAll(".orderDriver")
const driverTd = document.querySelectorAll(".driverTd")
const removeBtn = document.querySelectorAll(".removeBtn")
const dispatchBus = document.querySelectorAll(".dispatchBus")
const dispatchDriver = document.querySelectorAll(".dispatchDriver")
const hiddenBus = document.querySelectorAll(".hiddenBus")
const scheduleTableTr = document.querySelectorAll(".scheduleTableTr")



// 일반배차
for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", addOrderDispatch)
}


function addOrderDispatch() {
    if (popupAreaModulesDispatch.classList.contains("popupAreaModulesVisible")) {
        let targetBus = this

        let busNum = ""
        let busId = ""
        let DriverName = ""
        let DriverId = ""

        if (params.get("id") !== null) {
            if (!this.parentNode.classList.contains("haveSchedule")) {
                busNum = this.innerText.split("(")[0]
                busId = this.classList[1]
                DriverName = this.innerText.split("(")[1].replace(/\)/g, "")
                DriverId = this.classList[2].split("d")[1]
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

            // 배차
            function addOrderDispatch() {
                targetBus.parentNode.classList.add("haveSchedule")
                for (j = 0; j < dispatchLine.length; j++) {
                    if (dispatchLine[j].children[0].children[0].children[1].children[0].value == "") {
                        dispatchLine[j].children[0].children[0].children[1].children[0].value = busNum
                        dispatchLine[j].children[0].children[2].value = busId

                        const driverOption = document.createElement('option');
                        driverOption.setAttribute("value", `${DriverId}`);
                        driverOption.innerText = DriverName
                        orderDriver[j].appendChild(driverOption);
                        return
                    }
                }
            }


            //알림 출력
            if (beforeArr.length !== 0 || afterArr.length !== 0) {
                for (i = 0; i < beforeArr.length; i++) {
                    if (this.classList[1] == beforeArr[i].bus_id || this.classList[2] == `d${beforeArr[i].driver_id}`) {
                        if (confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${beforeArr[i].bus_num}(${beforeArr[i].driver_name}) || ${beforeArr[i].departure_date} ~ ${beforeArr[i].arrival_date}]`)) {
                            addOrderDispatch()
                            return
                        } else {
                            return
                        }
                    } else {
                        addOrderDispatch()
                        return
                    }
                }
                for (i = 0; i < afterArr.length; i++) {
                    if (this.classList[1] == afterArr[i].bus_id || this.classList[2] == `d${afterArr[i].driver_id}`) {
                        if (confirm(`운행종료 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${afterArr[i].bus_num}(${afterArr[i].driver_name}) || ${afterArr[i].departure_date} ~ ${afterArr[i].arrival_date}]`)) {
                            addOrderDispatch()
                            return
                        } else {
                            return
                        }
                    } else {
                        addOrderDispatch()
                        return
                    }
                }
            } else {
                addOrderDispatch()
                return
            }
        }
    }
}




// 배차 지우기
for (i = 0; i < removeBtn.length; i++) {
    removeBtn[i].addEventListener("click", deleteOrderDispatch)
}

function deleteOrderDispatch() {
    let dispatchCounter = ""
    for (i = 0; i < removeBtn.length; i++) {
        if (removeBtn[i] == this) {
            dispatchCounter = i
        }
    }
    for (i = 0; i < scheduleTableTr.length; i++) {
        if (scheduleTableTr[i].children[7].classList.contains(`${hiddenBus[dispatchCounter].value}`)) {
            scheduleTableTr[i].classList.remove("haveSchedule")
        }
    }
    dispatchBus[dispatchCounter].value = ""
    dispatchDriver[dispatchCounter].innerText = ""
    dispatchPrice[dispatchCounter].innerText = `${inputTextPrice.value}원`
    dispatchPaymen[dispatchCounter].innerText = `${inputTextDriverAllowance.value}원`
    hiddenBus[dispatchCounter].value = ""

}




let functionCounter = true;

// 배차가능 기사 옵션 추가
for (i = 0; i < orderDriver.length; i++) {
    orderDriver[i].addEventListener("click", addDriverOption);
}


function addDriverOption() {
    if (functionCounter == true || functionCounter !== this) {


        //배차가능 기사 필터링
        optionDriver = []

        for (i = 0; i < dataList.length; i++) {
            dataStartTime = dataList[i].departure_date.substr(0, 10).replace(/\-/g, "") + dataList[i].departure_date.substr(11, 5).replace(/\:/g, "")
            dataEndTime = dataList[i].arrival_date.substr(0, 10).replace(/\-/g, "") + dataList[i].arrival_date.substr(11, 5).replace(/\:/g, "")
            CreateCompareTime()
            // data기간 필터링
            if (dataEndTime >= inputStartTime && dataStartTime <= inputEndTime) {
                optionDriver.push(`${dataList[i].driver_id}`)
            }
        }

        // 등록하지 않고 선택만한 기사도 옵션에서 제거
        for (i = 0; i < dispatchLine.length; i++) {
            for (j = 0; j < dispatchLine[i].children[0].children[0].children[3].children[0].children.length; j++) {
                if (dispatchLine[i].children[0].children[0].children[3].children[0].children[j].selected) {
                    if (optionDriver.indexOf(dispatchLine[i].children[0].children[0].children[3].children[0].children[j].value) == -1) {
                        optionDriver.push(dispatchLine[i].children[0].children[0].children[3].children[0].children[j].value)
                    }
                }
            }
        }




        // 고정기사 저장

        let selectDriver = []
        if (this.children[0].value !== "") {
            for (i = 0; i < this.children.length; i++) {
                if (this.children[i].selected) {
                    selectDriver.push(this.children[i].value)
                    selectDriver.push(this.children[i].innerText)
                }
            }
        } else if (this.children[0].value == "" && this.children.length > 1) {
            selectDriver.push(this.children[1].value)
            selectDriver.push(this.children[1].innerText)
        }


        let useDriver = _.cloneDeep(driverObj)

        // // 배차불가 기사 제거
        for (i = 0; i < Object.keys(useDriver).length; i++) {
            for (j = 0; j < optionDriver.length; j++) {
                if (Object.keys(useDriver)[i] == optionDriver[j]) {
                    let deletKey = ""
                    deletKey = Object.keys(useDriver)[i]
                    delete useDriver[`${deletKey}`]
                }
            }
        }

        // 옵션 정렬
        let sortArr = []

        for (i = 0; i < Object.keys(useDriver).length; i++) {
            let sortObject = {
                name: `${Object.keys(useDriver)[i]}`,
                driver: `${Object.values(useDriver)[i]}`
            }
            sortArr.push(sortObject)
        }

        sortArr.sort(function (a, b) {
            return a.driver < b.driver ? -1 : a.driver > b.driver ? 1 : 0;
        });



        this.innerText = ""

        // // 선택옵션 빈칸/고정기사
        if (selectDriver.length !== 0) {

            // 선택기사 추가
            const firstOption = {
                name: `${selectDriver[0]}`,
                driver: `${selectDriver[1]}`
            }

            sortArr.unshift(firstOption)

        } else {
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", "");
            driverOption.innerText = ""
            this.appendChild(driverOption);
        }



        // 배차가능 기사 생성
        for (i = 0; i < Object.keys(sortArr).length; i++) {
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${sortArr[i].name}`);
            driverOption.innerText = sortArr[i].driver
            this.appendChild(driverOption);
        }

        functionCounter = this;

    } else {
        functionCounter = true;
    }

}






// 기사 변경시 배차간격 팝업
for (i = 0; i < dispatchDriver.length; i++) {
    dispatchDriver[i].addEventListener("change", rangePopup)
}


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