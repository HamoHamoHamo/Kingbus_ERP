const dispatchBtn = document.querySelector(".dispatchBtn")
const popupAreaModulesDispatch = document.querySelector(".popupAreaModulesDispatch")
const closeBtn = document.querySelector(".closeBtn")
const dispatchPopupData = document.querySelectorAll(".dispatcTable input")
const dispatchPriceBlank = document.querySelectorAll(".dispatchPriceBlank")
const dispatchPaymenBlank = document.querySelectorAll(".dispatchPaymenBlank")
const dispatchSave = document.querySelector(".dispatchSave")
const popupContainerDispatch = document.querySelector(".popupContainerDispatch")
const dispatchBox = document.querySelectorAll(".dispatchBox")



// 배차팝업 열기
dispatchBtn.addEventListener("click", openDispatch)

function openDispatch() {
    if (window.location.search.split("&")[0].substr(0, 3) == "?id") {
        if (scheduleOpenBtn.classList.contains("scheduleOpenBtnVisible")) {
            schedule.children[0].style.display = "flex"
            schedule.children[1].style.display = "flex"
            schedule.style.width = "36rem"
            MainLayout.style.width = "calc(100% - 38rem)"
            scheduleOpenBtn.classList.remove("scheduleOpenBtnVisible")
        }
        for (i = 0; i < dispatchPrice.length; i++) {
            dispatchPrice[i].value = dispatchPrice[i].value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
            dispatchPaymen[i].value = dispatchPaymen[i].value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
        popupAreaModulesDispatch.classList.add("popupAreaModulesVisible")
        for (i = 0; i < dispatchPriceBlank.length; i++) {
            dispatchPriceBlank[i].value = inputTextPrice.value
            dispatchPaymenBlank[i].value = inputTextDriverAllowance.value
        }
    }
}


// 배차팝업 닫기
closeBtn.addEventListener("click", dispatchPopupClose)

function dispatchPopupClose() {
    popupAreaModulesDispatch.classList.remove("popupAreaModulesVisible")
    for (i = 0; i < dispatchBox.length; i++) {
        dispatchBox[i].children[1].style.backgroundColor = "white"
    }
}

// 등록 필수 항목 검사
dispatchSave.addEventListener("click", dispatchSaveCheck)

function dispatchSaveCheck(e) {

    e.preventDefault()

    let selectDriver = []
    let selectOutSoursing = []

    for (i = 0; i < dispatchBox.length; i++) {
        if (dispatchBus[i].value !== "") {

            for (j = 0; j < orderDriver[i].children.length; j++) {
                if (orderDriver[i].children[j].selected && orderDriver[i].children[j].value !== "") {
                    selectDriver.push(true)
                }
            }

            for (j = 0; j < orderOutSoursing[i].children.length; j++) {
                if (orderOutSoursing[i].children[j].selected && orderOutSoursing[i].children[j].value !== "") {
                    selectOutSoursing.push(true)
                }
            }

        }
    }

    let selectBusCounter = 0

    for (i = 0; i < dispatchBus.length; i++) {
        if (dispatchBus[i].value !== "") {
            selectBusCounter = selectBusCounter + 1
        }
    };

    if (selectDriver.length + selectOutSoursing.length !== selectBusCounter) {
        return alert("담당기사를 배정해 주세요.")
    } else {
        return popupContainerDispatch.submit()
    }
}