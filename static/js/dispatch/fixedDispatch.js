const fixedDispatchText = document.querySelectorAll(".fixedDispatchText")
const fixedDispatchSelect = document.querySelectorAll(".fixedDispatchSelect")
const fixedDispatchInput = document.querySelectorAll(".fixedDispatchInput")
const driverTd = document.querySelectorAll(".driverTd")
const fixedDispatchDelete = document.querySelector(".fixedDispatchDelete")
const driveWeek = document.querySelectorAll(".driveDateBoxInput")
const getWeek = document.querySelectorAll(".fixedDispatchTable thead td")
const weekLabel = document.querySelectorAll(".driveDateBox label")
const fixedDispatchBox = document.querySelectorAll(".fixedDispatchBox")
const fixedDispatchWeek = document.querySelectorAll(".fixedDispatchTable thead td")



// 고정배차 선택시 색 변경

for (i = 0; i < fixedDispatchText.length; i++) {
    fixedDispatchText[i].addEventListener("click", clickFixedDispatch)
}

function clickFixedDispatch() {
    if (!this.classList.contains("disableToFixedDispatch")) {
        if (this.classList.contains("addDispatch")) {
            this.classList.remove("addDispatch")
            this.style.backgroundColor = "white"
            this.style.color = "black"
        } else {
            for (i = 0; i < fixedDispatchText.length; i++) {
                if (!fixedDispatchBox[i].classList.contains("disableToFixedDispatch")) {
                    fixedDispatchText[i].classList.remove("addDispatch")
                    fixedDispatchText[i].style.backgroundColor = "white"
                    fixedDispatchText[i].style.color = "black"
                }
            }
            this.classList.add("addDispatch")
            this.style.backgroundColor = "rgb(0, 105, 217)"
            this.style.color = "white"
            for (i = 0; i < scheduleRadio.length; i++) {
                scheduleRadio[i].checked = false
            }
            scheduleRadio[parseInt(this.parentNode.id.substr(13, 1)) - 1].checked = true
            radioDateChange()
        }
    }
}




// 선택가능한 요일
function ableFixedDispatch() {
    let ableFixedDispatchArr = []
    for (i = 0; i < 7; i++) {
        if (!driveWeek[i].checked) {
            ableFixedDispatchArr.push(weekLabel[i + 1].innerText)
        }
    }
    for (i = 0; i < fixedDispatchBox.length; i++) {
        for (j = 0; j < ableFixedDispatchArr.length; j++) {
            if (fixedDispatchWeek[i].innerText == ableFixedDispatchArr[j]) {
                fixedDispatchBox[i].classList.add("disableToFixedDispatch")
            }
        }
    }
}





// 고정배차

for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", fixedDispatch)
}

function fixedDispatch() {
    if (!this.parentNode.classList.contains("haveSchedule")) {
        for (j = 0; j < fixedDispatchText.length; j++) {
            if (fixedDispatchText[j].classList.contains("addDispatch")) {
                fixedDispatchText[j].classList.remove("addDispatch")
                fixedDispatchText[j].style.backgroundColor = "white"
                fixedDispatchText[j].style.width = "40%"
                fixedDispatchText[j].style.color = "black"
                fixedDispatchText[j].parentNode.children[1].style.display = "block"
                fixedDispatchText[j].innerText = this.innerText.substr(0, 4)
                fixedDispatchInput[j].value = this.classList[1]
                if (this.innerText.split("(")[1].replace(/\)/g, "") !== "") {
                    const driverOption = document.createElement('option');
                    driverOption.setAttribute("value", `${this.classList[2].split("d")[1]}`);
                    driverOption.innerText = this.innerText.split("(")[1].replace(/\)/g, "")
                    fixedDispatchText[j].parentNode.children[1].appendChild(driverOption);
                }
            }
        }
    } else {
        alert("배차 불가능한 차량입니다.")
    }
}






// 고정배차 삭제

fixedDispatchDelete.addEventListener("click", deleteFixedDispatch)

function deleteFixedDispatch() {
    for (i = 0; i < fixedDispatchText.length; i++) {
        if (fixedDispatchText[i].classList.contains("addDispatch")) {
            fixedDispatchText[i].classList.remove("addDispatch")
            fixedDispatchText[i].innerText = ""
            fixedDispatchText[i].style.backgroundColor = "white"
            fixedDispatchText[i].style.width = "100%"
            fixedDispatchText[i].style.color = "black"
            fixedDispatchText[i].parentNode.children[1].style.display = "none"
            fixedDispatchInput[i].value = ""
            for (j = 0; j < fixedDispatchText[i].parentNode.children[1].children.length; j++) {
                fixedDispatchText[i].parentNode.children[1].children[j].remove()
            }
        }
    }
}





// 고정배차 데이터 로드
function loadData() {
    let weekCheckerArr = ["일", "월", "화", "수", "목", "금", "토"];

    for (i = 0; i < data.length; i++) {
        if (data[i].route_id == window.location.search.split("id=")[1]) {
            for (j = 0; j < weekCheckerArr.length; j++) {
                if (data[i].week == weekCheckerArr[j]) {
                    fixedDispatchText[j].style.backgroundColor = "white"
                    fixedDispatchText[j].style.width = "40%"
                    fixedDispatchText[j].style.color = "black"
                    fixedDispatchText[j].parentNode.children[1].style.display = "block"
                    fixedDispatchText[j].innerText = data[i].bus_num
                    fixedDispatchInput[j].value = data[i].bus_id

                    const driverOption = document.createElement('option');
                    driverOption.setAttribute("value", `${data[i].driver_id}`);
                    driverOption.innerText = data[i].driver_name
                    fixedDispatchText[j].parentNode.children[1].appendChild(driverOption);
                }
            }
        }
    }
}







// 배차가능 기사 필터

for (i = 0; i < fixedDispatchSelect.length; i++) {
    fixedDispatchSelect[i].addEventListener("click", DispatcDriverFiilter)
}

function DispatcDriverFiilter() {

    if (this.children.length == 1) {
        
        scheduleBus = []

        // data요일 필터링
        for (i = 0; i < data.length; i++) {
            if (data[i].week == scheduleDay) {

                dataStartTime = data[i].departure_time.replace(/\:/g, "")
                dataEndTime = data[i].arrival_time.replace(/\:/g, "")

                // data기간 필터링
                if (dataEndTime >= inputStartTime && inputEndTime >= dataStartTime) {
                    scheduleBus.push(data[i].driver_id)
                }
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
