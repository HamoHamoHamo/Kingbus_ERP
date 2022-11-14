const loadDepositBtn = document.querySelector(".loadDepositBtn")
const routeRadio = document.querySelectorAll(".routeSelect")
const collectingPopupAreaModules = document.querySelector(".collectingPopupAreaModules")
const popupBgModulesCollect = document.querySelector(".popupBgModulesCollect")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const collectPopupCloseBtn = document.querySelector(".collectPopupCloseBtn")
const targetDeposit = document.querySelectorAll(".collectingPopupScrollBox tr")
const loadDate = document.querySelectorAll(".collectingPopupContainer .popupSearch input")
const loadDepositHidden = document.querySelector(".loadDepositHidden")

loadDepositBtn.addEventListener("click", loadDeposit)

function loadDeposit() {
    let selectRoute = false
    let routeId = ""
    for (i = 0; i < routeRadio.length; i++) {
        if (routeRadio[i].checked) {
            selectRoute = true
            routeId = routeRadio[i].parentNode.parentNode.classList[2]
            break;
        }
    };
    if (selectRoute) {
        collectingPopupAreaModules.style.display = "block"

        let today = new Date();

        let year = today.getFullYear();
        let month = today.getMonth() + 1;
        let date = today.getDate();

        loadDate[0].value = `${year}-${month}-${date}`
        loadDate[1].value = `${year}-${month}-${date}`

        loadDepositHidden.value = routeId

        let communicationData = {
            date1 : `${year}-${month}-${date}`,
            date2 : `${year}-${month}-${date}`,
        }
        console.log("TEST", communicationData);
        $.ajax({
            url: "/accounting/collect/load",
            method: "POST",
            data: JSON.stringify(communicationData),
            datatype: 'json',
            success: function (result) {
                if (result.status) {
                    result.deposit
                } else { 
                    alert("입금내역을 불러오지 못했습니다.")
                }
            },
            error: function (request, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            },
        });

    } else {
        alert("노선을 선택해 주세요")
    }
}

for (i = 0; i < collectDateBox.length; i++) {
    collectDateBox[i].addEventListener("click", routeSelecting)
};

function routeSelecting() {
    this.children[0].children[0].checked = true
}


//팝업닫기
popupBgModulesCollect.addEventListener("click", closePopup)
collectPopupCloseBtn.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    collectingPopupAreaModules.style.display = "none"
}



// 입금내역 선택
for (i = 0; i < targetDeposit.length; i++) {
    targetDeposit[i].addEventListener("click", selectDeposit)
};

function selectDeposit() {
    for (i = 0; i < targetDeposit.length; i++) {
        this.classList.remove("selectDepoditTr")
    };
    this.classList.add("selectDepoditTr")
}
