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
                if (confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${rangeBeforeArr[i].bus}(${rangeBeforeArr[i].driver}) || ${rangeBeforeArr[i].start} ~ ${rangeBeforeArr[i].end}]`)) {
                    rangeCounter = rangeCounter + 1
                }
            };
            for (i = 0; i < rangeAfterArr.length; i++) {
                if (confirm(`운행시작 1시간 이내에 노선이 있습니다. 배차하시겠습니까?\n[${rangeAfterArr[i].bus}(${rangeAfterArr[i].driver}) || ${rangeAfterArr[i].start} ~ ${rangeAfterArr[i].end}]`)) {
                    rangeCounter = rangeCounter + 1
                }
            };
        }

        if (rangeCounter == rangeBeforeArr.length + rangeAfterArr.length) {
            const businput= document.querySelector(".selectRoute input[type=text]")
            const driverSelect = document.querySelector(".selectRoute select[name=driver]")
            const busIdHidden = document.querySelector(".RouteList input[name=bus]")

            busNum = this.innerText.split("(")[0]
            busId = this.classList[1]
            DriverName = this.innerText.split("(")[1].replace(/\)/g, "")
            DriverId = this.classList[2].substr(1,)

            busInput.value = busNum;
            busIdHidden.value = busId;

            driverSelect.innerText = ""
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${DriverId}`);
            driverOption.innerText = DriverName
            driverSelect.appendChild(driverOption);
        }
    }
}

const businput= document.querySelector(".RouteListHBodyTr input[type=text]")
const driverSelect = document.querySelector(".RouteListHBodyTr select[name=driver]")
const outsorcingSelect = document.querySelector(".RouteListHBodyTr select[name=outsourcing]")


// 운전원&용역 하나만 선택
driverSelect.addEventListener("change", removeOutsourcing)

function removeOutsourcing(){
    outsorcingSelect.innerText = ""
}

outsorcingSelect.addEventListener("change", removeDrive)

function removeDrive(){
    driverSelect.innerText = ""
}




// 운전원 옵션

let useSelect = true;

// 배차가능 기사 필터(기사-옵션)
driverSelect.addEventListener("click", addDriverOption);

function addDriverOption() {
    if (busInput.value !== "") {
        if (useSelect == true || useSelect !== this) {

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

            for (i = 0; i < data.length; i++) {
                let dataStartTime = ""
                let dataEndTime = ""
                if (data[i].outSoursing !== "y") {
                    dataStartTime = data[i].departure_date.split(" ")[1].replace(/\:/g, "")
                    dataEndTime = data[i].arrival_date.split(" ")[1].replace(/\:/g, "")
                } else {
                    dataStartTime = data[i].departure_date.split(" ")[1].replace(/\:/g, "")
                    dataEndTime = data[i].arrival_date.split(" ")[1].replace(/\:/g, "")
                }
                if (dataEndTime >= inputStartTime && dataStartTime <= inputEndTime) {
                    periodFilter.push(`${data[i].driver_id}`)
                }
            }

            // 4. 배차가능 기사 추출 -> 기사데이터 - 3번

            let useDriver = []

            for (i = 0; i < Object.keys(driverObj).length; i++) {
                useDriver.push(Object.keys(driverObj)[i])
            }

            for (i = 0; i < periodFilter.length; i++) {
                useDriver = useDriver.filter(current => current !== periodFilter[i])
            }

            // 4-2. 배차가능 기사 추출 -> 현재 선택기사 제거
            useDriver = useDriver.filter(current => current !== firstOption[0])

            // 5. 배차가능 배열 오브젝트로 변경

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

            // 6. 배차가능 오브젝트 정렬

            useDriverSort.sort(function (a, b) {
                return a.driver < b.driver ? -1 : a.driver > b.driver ? 1 : 0;
            });

            // 7. 첫번째 옵션 생성 -> 1번

            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${firstOption[0]}`);
            driverOption.innerText = `${firstOption[1]}`
            this.appendChild(driverOption);

            // 8. 선택가능 기사 옵션 생성 -> 5번

            for (i = 0; i < useDriverSort.length; i++) {
                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${useDriverSort[i].name}`);
                driverOption.innerText = `${useDriverSort[i].driver}`
                this.appendChild(driverOption);
            }

            useSelect = this
        } else {
            useSelect = true
        }
        useOutSoursing = true
    }
}




// 용역 옵션

let useOutsourcingSelect = true;

// 배차가능 기사 필터(기사-옵션)
outsorcingSelect.addEventListener("click", addorderOutSoursingOption);

function addorderOutSoursingOption() {
    if (busInput.value !== "") {
        if (useOutsourcingSelect == true || useOutsourcingSelect !== this) {

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

            for (i = 0; i < data.length; i++) {
                let dataStartTime = ""
                let dataEndTime = ""
                if (data[i].outSoursing !== "y") {
                    dataStartTime = data[i].departure_date.split(" ")[1].replace(/\:/g, "")
                    dataEndTime = data[i].arrival_date.split(" ")[1].replace(/\:/g, "")
                } else {
                    dataStartTime = data[i].departure_date.split(" ")[1].replace(/\:/g, "")
                    dataEndTime = data[i].arrival_date.split(" ")[1].replace(/\:/g, "")
                }
                if (dataEndTime >= inputStartTime && dataStartTime <= inputEndTime) {
                    periodFilter.push(`${data[i].driver_id}`)
                }
            }

            // 4. 배차가능 기사 추출 -> 기사데이터 - 3번

            let useDriver = []

            for (i = 0; i < Object.keys(outsourcingObj).length; i++) {
                useDriver.push(Object.keys(outsourcingObj)[i])
            }

            for (i = 0; i < periodFilter.length; i++) {
                useDriver = useDriver.filter(current => current !== periodFilter[i])
            }

            // 4-2. 배차가능 기사 추출 -> 현재 선택기사 제거
            useDriver = useDriver.filter(current => current !== firstOption[0])

            // 5. 배차가능 배열 오브젝트로 변경

            let useDriverSort = []

            for (i = 0; i < Object.keys(outsourcingObj).length; i++) {
                for (j = 0; j < useDriver.length; j++) {
                    if (Object.keys(outsourcingObj)[i] == useDriver[j]) {
                        let useDriveObj = {
                            name: `${Object.keys(outsourcingObj)[i]}`,
                            driver: `${Object.values(outsourcingObj)[i]}`
                        }
                        useDriverSort.push(useDriveObj)
                    }
                }
            }

            // 6. 배차가능 오브젝트 정렬

            useDriverSort.sort(function (a, b) {
                return a.driver < b.driver ? -1 : a.driver > b.driver ? 1 : 0;
            });

            // 7. 첫번째 옵션 생성 -> 1번

            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${firstOption[0]}`);
            driverOption.innerText = `${firstOption[1]}`
            this.appendChild(driverOption);

            // 8. 선택가능 기사 옵션 생성 -> 5번

            for (i = 0; i < useDriverSort.length; i++) {
                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${useDriverSort[i].name}`);
                driverOption.innerText = `${useDriverSort[i].driver}`
                this.appendChild(driverOption);
            }

            useOutsourcingSelect = this
        } else {
            useOutsourcingSelect = true
        }
        useSelect = true
    }
}