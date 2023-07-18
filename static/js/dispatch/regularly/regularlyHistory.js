const popup = document.querySelector(".popupAreaModules")
const popupBg = document.querySelector(".popupBgModules")
const dispatchHistory = document.querySelector(".dispatchHistory")
const popupCloseBtn = document.querySelector(".popupCloseBtn")
const historyDateBox = document.querySelectorAll(".historyDateBox")
const historyHiddenRoute = document.querySelector(".historyHiddenRoute")
const historyHiddenBus = document.querySelector(".historyHiddenBus")
const historyHiddenDriver = document.querySelector(".historyHiddenDriver")
const historyHiddenGroup = document.querySelector(".historyHiddenGroup")
const historyHiddenDate = document.querySelector(".historyHiddenDate")
const historyHiddenOutsourcing = document.querySelector(".historyHiddenOutsourcing")
const popupContainerDispatchHistory = document.querySelector(".popupContainerDispatchHistory")
const loadHistory = document.querySelector(".loadHistory")
const loadingBg = document.querySelector(".loadingBg")

const loadConnectBtn1 = document.querySelector(".loadConnectBtn1")
const loadConnectBtn2 = document.querySelector(".loadConnectBtn2")

// 지난배차 불러오기
loadConnectBtn1.addEventListener('click', () => loadConnect(7))

loadConnectBtn2.addEventListener('click', () => loadConnect(1))

function loadConnect(type) {
    const formValues = $('.RouteList').serialize();
    loadingBg.style.display = "flex";
    $.ajax({
        url: `regularly/connect/load/${type}`,
        method: "POST",
        data: formValues,
        datatype: 'json',
        success: function (data) {
            console.log("DATASS", data);
            // 중복 배차일 경우
            if (data['status'] === 'overlap') {
                alert(`${data.route}의 지난 배차를 불러올 수 없습니다`)
                loadingBg.style.display = "none";
                location.reload();
            } else if (data['status'] === 'check') {
                alert('노선을 선택해 주세요.')
                loadingBg.style.display = "none";
            } else {
                alert('배차가 저장되었습니다.');
                location.reload();
            }
        },
        error: function (request, status, error) {
            alert(`${data.route}의 지난 배차를 불러올 수 없습니다`)
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            loadingBg.style.display = "none";
        },
    });
}


// 배차내역 열기
dispatchHistory.addEventListener("click", openDispatchHistory)

function openDispatchHistory() {
    if (window.location.search !== "") {
        let queryId = window.location.search.split("id=")[1].split("&")[0]
        if (queryId !== "") {
            popup.style.display = "block"
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
for (i = 0; i < historyDateBox.length; i++) {
    historyDateBox[i].addEventListener("click", HistoryCheck)
}

function HistoryCheck() {
    if(!this.classList.contains("historyUnable")){
        let parms = new URLSearchParams(location.search)
        // historyHiddenRoute.value = parms.get("id")
        historyHiddenGroup.value = parms.get("group")
        historyHiddenDate.value = parms.get("date")
        if (this.classList.contains("historyDateBoxSelect")) {
            for (i = 0; i < historyDateBox.length; i++) {
                historyDateBox[i].classList.remove("historyDateBoxSelect")
            }
            this.classList.remove("historyDateBoxSelect")
            historyHiddenBus.value = ""
            historyHiddenDriver.value = ""
            historyHiddenOutsourcing.value = ""
        } else {
            for (i = 0; i < historyDateBox.length; i++) {
                historyDateBox[i].classList.remove("historyDateBoxSelect")
            }
            this.classList.add("historyDateBoxSelect")
            historyHiddenBus.value = this.children[1].classList[1]
            if (this.children[2].classList[2] === "typeOutsourcing") {
                historyHiddenDriver.value = ""
                historyHiddenOutsourcing.value = this.children[2].classList[1]
            }else{
                historyHiddenDriver.value = this.children[2].classList[1]
                historyHiddenOutsourcing.value = ""
            }
        }
    }
}




loadHistory.addEventListener("click", loadHistoryftn)

function loadHistoryftn(){
    if(historyHiddenBus.value === ""){
        return alert("선택된 배차내역이 없습니다")
    }else{
        popupContainerDispatchHistory.submit()
    }
}