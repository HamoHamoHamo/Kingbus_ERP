const scheduleListCloseBtn = document.querySelector(".scheduleListCloseBtn")


function openScheduleList() {
    popupAreaModules[3].style.display = "block"
}

popupBgModules[3].addEventListener("click", closeScheduleList)
SidemenuUseClose.addEventListener("click", closeScheduleList)
scheduleListCloseBtn.addEventListener("click", closeScheduleList)

function closeScheduleList() {
    popupAreaModules[3].style.display = "none"
}