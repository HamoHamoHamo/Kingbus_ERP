let params = new URLSearchParams(document.location.search)

const searchRoute = document.querySelector("input[name=route]")
const orderSearchSelect = document.querySelector(".orderSearchSelect")

window.onload = function () {
    inputToDay()
    matchHeight()
    drawSchdule()
    DispatcBusFilter()
    // notPairFilter()
    addCommaList()
    changeVAT()
    listHeight()
    thisRoute()
    matchDispatch()
    addCommaTotal()

    if(params.has("date1") && !params.has("id")){
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
    if(params.has("type")){
        if(params.get("type") === "customer"){
            for (i = 0; i < orderSearchSelect.children.length; i++){
                if(orderSearchSelect.children[i].innerText === "예약자"){
                    orderSearchSelect.children[i].selected = true
                }
            };            
        }
    }
}



let inputStartTime = ""
let inputEndTime = ""