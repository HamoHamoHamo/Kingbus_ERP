const loadDepositBtn = document.querySelector(".loadDepositBtn")
const routeRadio = document.querySelectorAll(".routeSelect")
const collectingPopupAreaModules = document.querySelector(".collectingPopupAreaModules")
const popupBgModulesCollect = document.querySelector(".popupBgModulesCollect")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const collectPopupCloseBtn = document.querySelector(".collectPopupCloseBtn")
const targetDeposit = document.querySelectorAll(".collectingPopupScrollBox tr")

loadDepositBtn.addEventListener("click", loadDeposit)

function loadDeposit() {
    let selectRoute = false
    for (i = 0; i < routeRadio.length; i++) {
        if (routeRadio[i].checked) {
            selectRoute = true
            break;
        }
    };
    if (selectRoute) {
        collectingPopupAreaModules.style.display = "block"
    }else{
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
for (i = 0; i < targetDeposit.length; i++){
    targetDeposit[i].addEventListener("click", selectDeposit)
};

function selectDeposit(){
    for (i = 0; i < targetDeposit.length; i++){
        this.classList.remove("selectDepoditTr")
    };    
    this.classList.add("selectDepoditTr")
}
