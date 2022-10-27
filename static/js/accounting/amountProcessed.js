const amountProcessed = document.querySelector(".depositDateTable td:nth-child(9)")
const amountProcessedCloseBtn = document.querySelector(".amountProcessedCloseBtn")

amountProcessed.addEventListener("click", openPopup)

function openPopup(){
    popupAreaModules[1].style.display = "block"
}

popupBgModules[1].addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
amountProcessedCloseBtn.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules[1].style.display = "none"
}