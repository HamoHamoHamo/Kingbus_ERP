const crete = document.querySelector(".popup-area-box_btn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const popupCloseBtn = document.querySelector(".popupCloseBtn")
const SidemenuUseClose = document.querySelector(".Sidemenu")

crete.addEventListener("click", openCreatePopup)

function openCreatePopup(){
    popupAreaModules.style.display = "block"
}

popupBgModules.addEventListener("click", closePopup)
popupCloseBtn.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules.style.display = "none"
}