const fixedDispatchText = document.querySelectorAll(".fixedDispatchText")
const fixedDispatchSelect = document.querySelectorAll(".fixedDispatchSelect")
const fixedDispatchInput = document.querySelectorAll(".fixedDispatchInput")
const driverTd = document.querySelectorAll(".driverTd")
const fixedDispatchDelete = document.querySelector(".fixedDispatchDelete")
const driveWeek = document.querySelectorAll(".driveDateBoxInput")
const getWeek = document.querySelectorAll(".fixedDispatchTable thead td")



// 고정배차 선택시 색 변경

for (i = 0; i < fixedDispatchText.length; i++) {
    fixedDispatchText[i].addEventListener("click", clickFixedDispatch)
}

function clickFixedDispatch() {
    if (this.classList.contains("addDispatch")) {
        this.classList.remove("addDispatch")
        this.style.backgroundColor = "white"
        this.style.color = "black"
    } else {
        for (i = 0; i < fixedDispatchText.length; i++) {
            fixedDispatchText[i].classList.remove("addDispatch")
            if (fixedDispatchText[i].classList.contains("ableWeek")) {
                fixedDispatchText[i].style.backgroundColor = "white"
            }
            fixedDispatchText[i].style.color = "black"
        }
        this.classList.add("addDispatch")
        this.style.backgroundColor = "rgb(0, 105, 217)"
        this.style.color = "white"
        for (i = 0; i < scheduleRadio.length; i++) {
            scheduleRadio[i].checked = false
        }
        scheduleRadio[parseInt(this.parentNode.id.substr(13, 1)) - 1].checked = true
        callSchedule()
    }
}



// 고정배차에 기사 추가

for (i = 0; i < driverTd.length; i++) {
    driverTd[i].addEventListener("click", addFixedDispatch)
}

function addFixedDispatch(e) {
    const addDispatch = document.querySelectorAll(".addDispatch")
    if (window.location.search !== "") {
        if (!this.classList.contains("haveSchedule")) {
            for (i = 0; i < addDispatch.length; i++) {
                if (addDispatch[i].classList.contains("ableWeek")) {
                    addDispatch[i].parentNode.children[0].innerText = this.innerText.substr(0, 4)
                    addDispatch[i].parentNode.children[2].value = this.classList[1]
                    addDispatch[i].classList.remove("addDispatch")
                    addDispatch[i].style.backgroundColor = "white"
                    addDispatch[i].style.width = "40%"
                    addDispatch[i].style.color = "black"
                    addDispatch[i].parentNode.children[1].style.display = "block"

                    // 옵션 생성
                    const removeOption = addDispatch[i].parentNode.children[1].querySelectorAll(".fixedDispatchSelect option")
                    for (j = 0; j < removeOption.length; j++) {
                        removeOption[j].remove()
                    }

                    const driverOption = document.createElement('option');
                    driverOption.setAttribute("value", `${e.target.classList[2]}`);
                    driverOption.innerText = driverObj[e.target.classList[2]]
                    addDispatch[i].parentNode.children[1].appendChild(driverOption);

                    for (j = 0; j < addDispatch[i].parentNode.children[1].children.length; j++) {
                        if (addDispatch[i].parentNode.children[1].children[j].innerText == e.target.innerText.split("(")[1].replace(/\)/g, "")) {
                            addDispatch[i].parentNode.children[1].children[j].selected = true
                        }
                    }

                } else {
                    alert("배차 가능한 요일이 아닙니다.")
                }
            }
        }
    }
}



// 고정배차 삭제

fixedDispatchDelete.addEventListener("click", deleteFixedDispatch)

function deleteFixedDispatch() {
    for (i = 0; i < fixedDispatchInput.length; i++) {
        if (fixedDispatchInput[i].classList.contains("addDispatch")) {
            fixedDispatchInput[i].id = ""
        }
    }
}




// 셀렉트 선택
for (i = 0; i < fixedDispatchSelect.length; i++) {
    fixedDispatchSelect[i].addEventListener("click", selectCheck)
}

function selectCheck(e) {
    if (e.target.parentNode.children[0].classList.contains("addDispatch")) {
        e.target.parentNode.children[0].classList.remove("addDispatch")
        e.target.parentNode.children[0].style.backgroundColor = "white"
        e.target.parentNode.children[0].style.color = "black"
    } else {
        for (i = 0; i < fixedDispatchText.length; i++) {
            fixedDispatchText[i].classList.remove("addDispatch")
            if (fixedDispatchText[i].classList.contains("ableWeek")) {
                fixedDispatchText[i].style.backgroundColor = "white"
            }
            fixedDispatchText[i].style.color = "black"
        }
        e.target.parentNode.children[0].classList.add("addDispatch")
        e.target.parentNode.children[0].style.backgroundColor = "rgb(0, 105, 217)"
        e.target.parentNode.children[0].style.color = "white"
        for (i = 0; i < scheduleRadio.length; i++) {
            scheduleRadio[i].checked = false
        }
        scheduleRadio[parseInt(e.target.parentNode.children[0].parentNode.id.substr(13, 1)) - 1].checked = true
        callSchedule()
    }
    if (!this.classList.contains("fullOption")) {
        let driverOptionArr = []
        let idOptionArr = []
        for (i = 0; i < driverTd.length; i++) {
            if (driverTd[i].classList.contains("ableToDispatch")) {
                driverOptionArr.push(driverObj[driverTd[i].classList[2]])
                idOptionArr.push(driverTd[i].classList[2])
            }
        }
        let setDriverOptionArr = new Set(driverOptionArr)
        driverOptionArr = [...setDriverOptionArr]
        driverOptionArr = driverOptionArr.filter(current => current !== this.children[0].innerText)
        let setIdOptionArr = new Set(idOptionArr)
        idOptionArr = [...setIdOptionArr]
        idOptionArr = idOptionArr.filter(current => current !== this.children[0].value)
        for (i = 0; i < driverOptionArr.length; i++) {
            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${idOptionArr[i]}`);
            driverOption.innerText = driverOptionArr[i]
            this.appendChild(driverOption);
        }
        this.classList.add("fullOption")
    }
}



// 고정배차 데이터 넣기
function loadData() {
    for (i = 0; i < connect.length; i++) {
        for (j = 0; j < getWeek.length; j++) {
            if (connect[i].week == getWeek[j].innerText) {
                fixedDispatchText[j].innerText = connect[i].bus
                fixedDispatchInput[j].value = connect[i].bus_id
                fixedDispatchText[j].style.backgroundColor = "white"
                fixedDispatchText[j].style.width = "40%"
                fixedDispatchText[j].style.color = "black"
                fixedDispatchSelect[j].style.display = "block"
                const loadOption = document.createElement('option');
                loadOption.setAttribute("value", `${connect[i].driver_id}`);
                loadOption.innerText = connect[i].driver
                fixedDispatchSelect[j].appendChild(loadOption);
            }
        }
    }
}






// 고정배차 삭제
fixedDispatchDelete.addEventListener("click", deleteDispatch)

function deleteDispatch() {
    let deleteAlert = true
    for (i = 0; i < fixedDispatchText.length; i++) {
        if (fixedDispatchText[i].classList.contains("addDispatch")) {
            deleteAlert = false
            fixedDispatchText[i].innerText = ""
            for (j = 0; j < fixedDispatchText[i].parentNode.children[1].children.length; j++) {
                fixedDispatchText[i].parentNode.children[1].children[j].remove()
            }
            fixedDispatchText[i].parentNode.children[2].value = ""
            fixedDispatchText[i].style.backgroundColor = "white"
            fixedDispatchText[i].style.width = "100%"
            fixedDispatchText[i].style.color = "black"
            fixedDispatchText[i].classList.remove("addDispatch")
            fixedDispatchText[i].parentNode.children[1].style.display = "none"
        }
    }
    if(deleteAlert){
        alert("삭제할 배차를 선택해 주세요.")
    }
}