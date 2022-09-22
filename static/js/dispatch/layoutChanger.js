const schedule = document.querySelector(".schedule")
const scheduleCloseBtn = document.querySelector(".scheduleCloseBtn")
const scheduleOpenBtn = document.querySelector(".scheduleOpenBtn")
const MainLayout = document.querySelector(".MainLayout")


// 스케줄 닫기
scheduleCloseBtn.addEventListener("click", scheduleClose)

function scheduleClose(){
        schedule.children[0].style.display = "none"
        schedule.children[1].style.display = "none"
        schedule.style.width = "6rem"
        MainLayout.style.width = "calc(100% - 8rem)"
        scheduleOpenBtn.classList.add("scheduleOpenBtnVisible")
}



// 스케줄 열기
scheduleOpenBtn.addEventListener("click", scheduleOpen)

function scheduleOpen(){
    schedule.children[0].style.display = "flex"
    schedule.children[1].style.display = "flex"
    schedule.style.width = "36rem"
    MainLayout.style.width = "calc(100% - 38rem)"
    scheduleOpenBtn.classList.remove("scheduleOpenBtnVisible")
}