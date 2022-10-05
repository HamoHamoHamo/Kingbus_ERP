const groupList = document.querySelector(".groupList")
const groupClose = document.querySelector(".groupListHeadBtnBox svg:nth-child(1)")
const changeSchedule = document.querySelector(".groupListHeadBtnBox svg:nth-child(2)")
const schedule = document.querySelector(".schedule")
const scheduleClose = document.querySelector(".scheduleHeaderBtnBox svg:nth-child(1)")
const changeGroup = document.querySelector(".scheduleHeaderBtnBox svg:nth-child(2)")
const sideLayoutOpenBox = document.querySelector(".sideLayoutOpenBox")
const openScheduleBtn = document.querySelector(".scheduleOpenArea")
const openGroupBtn = document.querySelector(".GroupOpenArea")
const sideLayout = document.querySelector(".sideLayout")
const mainLayout = document.querySelector(".mainLayout")


// 스케줄 -> 그룹
changeGroup.addEventListener("click", scheduleToGroup)

function scheduleToGroup(){
    schedule.style.display = "none"
    groupList.style.display = "flex"
}


// 스케줄 닫기
scheduleClose.addEventListener("click", closeSchedule)

function closeSchedule(){
    schedule.style.display = "none"
    sideLayoutOpenBox.style.display = "flex"
    sideLayout.style.width = "6rem"
    mainLayout.style.width = "calc(100% - 8rem)"
}



// 스케줄 열기
openScheduleBtn.addEventListener("click", openSchedule)

function openSchedule(){
    schedule.style.display = "flex"
    sideLayoutOpenBox.style.display = "none"
    sideLayout.style.width = "36rem"
    mainLayout.style.width = "calc(100% - 38rem)"
}


// 그룹 -> 스케줄
changeSchedule.addEventListener("click", groupToSchedule)

function groupToSchedule(){
    groupList.style.display = "none"
    schedule.style.display = "flex"
}


// 그룹 닫기
groupClose.addEventListener("click", closeGroup)

function closeGroup(){
    groupList.style.display = "none"
    sideLayoutOpenBox.style.display = "flex"
    sideLayout.style.width = "6rem"
    mainLayout.style.width = "calc(100% - 8rem)"
}



// 그룹 열기
openGroupBtn.addEventListener("click", openGroup)

function openGroup(){
    groupList.style.display = "flex"
    sideLayoutOpenBox.style.display = "none"
    sideLayout.style.width = "36rem"
    mainLayout.style.width = "calc(100% - 38rem)"
}