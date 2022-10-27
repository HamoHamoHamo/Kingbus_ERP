const vhicleCheck = document.querySelector(".vhicleCheck")
const inspectionCloseBtn = document.querySelector(".inspectionCloseBtn")



vhicleCheck.addEventListener("click", openInspection)

function openInspection() {
    if (this.classList.contains("alarmAble")) {
        popupAreaModules[2].style.display = "block"
    }
}

popupBgModules[2].addEventListener("click", closeInspection)
SidemenuUseClose.addEventListener("click", closeInspection)
inspectionCloseBtn.addEventListener("click", closeInspection)

function closeInspection() {
    popupAreaModules[2].style.display = "none"
}