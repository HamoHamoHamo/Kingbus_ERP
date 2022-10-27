let params = new URLSearchParams(document.location.search)

const searchRoute = document.querySelector("input[name=route]")

window.onload = function () {
    inputToDay()
    matchHeight()
    drawSchdule()
    DispatcBusFilter()
    notPairFilter()
    addCommaList()
    changeVAT()
    pageLoadAddComma()
    listHeight()
    thisRoute()
    matchDispatch()

    if(params.has("date1")){
        inputTextquarter[0].value = params.get("date1")
        inputTextquarter[1].value = params.get("date1")
    }else if(!window.location.search){
        inputTextquarter[0].value = searchDate[0].value
        inputTextquarter[1].value = searchDate[0].value
    }
    if(params.has("route")){
        searchRoute.value = params.get("route")
    }
    if(params.has("close")){
        schedule.children[0].style.display = "none"
        schedule.children[1].style.display = "none"
        schedule.style.width = "6rem"
        MainLayout.style.width = "calc(100% - 8rem)"
        scheduleOpenBtn.classList.add("scheduleOpenBtnVisible")
    }
}



let inputStartTime = ""
let inputEndTime = ""