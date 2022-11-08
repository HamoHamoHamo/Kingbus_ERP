const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const checkerCloseBtn = document.querySelector(".checkerCloseBtn")
const addChecker = document.querySelector(".addChecker")
const checkDateData = document.querySelector(".checkDateData")
const checkForm = document.querySelector(".checkForm")

window.onload = function () {
    const checkMark = document.querySelectorAll(".checkMark")


    for (i = 0; i < checkMark.length; i++) {
        checkMark[i].addEventListener("click", openChecker)
    };

    function openChecker() {
        popupAreaModules[0].style.display = "block"
    }

    const scheduleList = document.querySelectorAll(".dataCellCalender")


    for (i = 0; i < scheduleList.length; i++) {
        scheduleList[i].addEventListener("click", openScheduleList)
    };

    
    const calnderItem = document.querySelectorAll(".calnderItem")
    sliceLength(calnderItem)
}


addChecker.addEventListener("click", Checking)

function Checking() {
    checkDateData.value = thisDateData
    checkForm.submit()
}



popupBgModules[0].addEventListener("click", closeChecker)
SidemenuUseClose.addEventListener("click", closeChecker)
checkerCloseBtn.addEventListener("click", closeChecker)

function closeChecker() {
    popupAreaModules[0].style.display = "none"
}