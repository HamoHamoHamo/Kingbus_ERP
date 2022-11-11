const depositRegistrationBtn = document.querySelector(".depositRegistrationBtn")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelector(".popupCloseBtn")

depositRegistrationBtn.addEventListener("click", openPopup)

function openPopup(){
    popupAreaModules[0].style.display = "block"
}

popupBgModules[0].addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
popupCloseBtn.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules[0].style.display = "none"
}