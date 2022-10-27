const scheduleCloseBtn = document.querySelector(".scheduleCloseBtn")
const addSchedule = document.querySelector(".addSchedule")
const addScheduleBtn = document.querySelector(".addScheduleBtn")
const scheduleDateData = document.querySelector(".scheduleDateData")
const scheduleForm = document.querySelector(".scheduleForm")
const scheduleDate = document.querySelector(".scheduleDate")
const scheduleContents = document.querySelector(".scheduleContents")

addSchedule.addEventListener("click", openSchedulePopup)

function openSchedulePopup(){
    popupAreaModules[1].style.display = "block"
}

addScheduleBtn.addEventListener("click", createSchedule)

function createSchedule(){
    scheduleDateData.value = thisDateData
    scheduleForm.submit()
}

popupBgModules[1].addEventListener("click", closeAddSchedule)
SidemenuUseClose.addEventListener("click", closeAddSchedule)
scheduleCloseBtn.addEventListener("click", closeAddSchedule)

function closeAddSchedule(){
    popupAreaModules[1].style.display = "none"
    scheduleDate.value = ""
    scheduleContents.value = ""
}