const dispatchBtn = document.querySelector(".dispatchBtn")
const popupAreaModulesDispatch = document.querySelector(".popupAreaModulesDispatch")
const closeBtn = document.querySelector(".closeBtn")
const dispatchPopupData = document.querySelectorAll(".dispatcTable input")
const dispatchPriceBlank = document.querySelectorAll(".dispatchPriceBlank")
const dispatchPaymenBlank = document.querySelectorAll(".dispatchPaymenBlank")
const dispatchSave = document.querySelector(".dispatchSave")
const popupContainerDispatch = document.querySelector(".popupContainerDispatch")



// 배차팝업 열기
dispatchBtn.addEventListener("click", openDispatch)

function openDispatch() {
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


// 배차팝업 닫기
closeBtn.addEventListener("click", dispatchPopupClose)

function dispatchPopupClose() {
    popupAreaModulesDispatch.classList.remove("popupAreaModulesVisible")
}

// 등록 필수 항목 검사
dispatchSave.addEventListener("click", dispatchSaveCheck)

function dispatchSaveCheck(e) {
    e.preventDefault()

    let selectDriver = []

    for (i = 0; i < removeBtn.length; i++) {
        if (dispatchBus.value !== "") {
            for (j = 0; j < dispatchDriver[i].children.length; j++) {
                if (dispatchDriver[i].children[j].selected) {
                    selectDriver.push(dispatchDriver[i].children[j].value)
                }
            }
        }
    }

    for (i = 0; i < selectDriver.length; i++) {
        if (selectDriver[i] == "") {
            return alert("담당기사를 배정해 주세요.")
        }
    }
    return popupContainerDispatch.submit()
}