const history = document.querySelectorAll(".collectDateBox td:nth-child(12)")
const historyPopupAreaModules = document.querySelector(".historyPopupAreaModules")
const popupBgModulesHistory = document.querySelector(".popupBgModulesHistory")
const historyPopupCloseBtn = document.querySelector(".historyPopupCloseBtn")

for (i = 0; i < history.length; i++){
    history[i].addEventListener("click", openHistory)
};

function openHistory(){
    historyPopupAreaModules.style.display = "block"
    
}



//팝업닫기
popupBgModulesHistory.addEventListener("click", closePopupHistory)
historyPopupCloseBtn.addEventListener("click", closePopupHistory)
SidemenuUseClose.addEventListener("click", closePopupHistory)


function closePopupHistory() {
    historyPopupAreaModules.style.display = "none"
}