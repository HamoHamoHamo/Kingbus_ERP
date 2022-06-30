const scheduleDriver = document.querySelectorAll('.scheduleTableBody td:nth-child(25)')
const popupAreaModules = document.querySelector('.popupAreaModules')
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelector(".PopupBtnBox div")


for (i = 0; i < scheduleDriver.length; i++) {
    scheduleDriver[i].addEventListener('click', openScheduleDetail)
}

function openScheduleDetail() {
    popupAreaModules.style.display = 'block'
}

popupBgModules.addEventListener('click', closePopupToBg)
SidemenuUseClose.addEventListener('click', closePopupToSideMenu)
popupCloseBtn.addEventListener('click', closePopupToBtn)

function closePopupToBg(){
    popupAreaModules.style.display = 'none'
}

function closePopupToSideMenu(){
    popupAreaModules.style.display = 'none'
}

function closePopupToBtn(){
    popupAreaModules.style.display = 'none'
}