const popup = document.querySelector(".popupAreaModules")
const popupBg = document.querySelector(".popupBgModules")
const dispatchHistory = document.querySelector(".dispatchHistory")
const popupCloseBtn = document.querySelector(".popupCloseBtn")
const historyItem = document.querySelectorAll(".historyItem")
const historyHiddenRoute = document.querySelector(".historyHiddenRoute")
const historyHiddenBus = document.querySelector(".historyHiddenBus")
const historyHiddenDriver = document.querySelector(".historyHiddenDriver")




// 배차내역 열기
dispatchHistory.addEventListener("click", openDispatchHistory)

function openDispatchHistory() {
    if (window.location.search !== "") {
        let queryId = window.location.search.split("id=")[1].split("&")[0]
        if (queryId !== "") {
            popup.style.display = "block"
            historyHidden.value = queryId
        }
    }
}



// 배차내역 닫기
popupBg.addEventListener("click", closeDispatchHistory)
Sidemenu.addEventListener("click", closeDispatchHistory)
popupCloseBtn.addEventListener("click", closeDispatchHistory)

function closeDispatchHistory() {
    popup.style.display = "none"
}



// 배차내역 선택
for (i = 0; i < historyItem.length; i++) {
    historyItem[i].addEventListener("click", HistoryCheck)
}

function HistoryCheck() {
    if (this.classList.contains("checkHistoryItem")) {
        for (i = 0; i < historyItem.length; i++) {
            historyItem[i].classList.remove("checkHistoryItem")
        }
        this.classList.remove("checkHistoryItem")
    } else {
        for (i = 0; i < historyItem.length; i++) {
            historyItem[i].classList.remove("checkHistoryItem")
        }
        this.classList.add("checkHistoryItem")
    }
    historyHiddenBus.value = this.children[0].classList[1]
    historyHiddenDriver.value = this.children[1].classList[1]
}