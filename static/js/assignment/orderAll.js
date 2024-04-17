let params = new URLSearchParams(document.location.search)

const searchRoute = document.querySelector("input[name=route]")
const orderSearchSelect = document.querySelector(".orderSearchSelect")
const inputTextPrice = document.querySelector(".inputTextPrice")
const inputTextDriverAllowance = document.querySelector(".inputTextDriverAllowance")

const clickRoute = document.querySelectorAll(".listTableScroll .ListTableBox tr")
const orderListMain = document.querySelectorAll(".orderListMain .orderListScrollBox .orderListItem")
const clickToDetail = document.querySelectorAll(".clickToDetail")


for (i = 0; i < orderListMain.length; i++) {
    orderListMain[i].addEventListener("mouseover", ListOver)
    orderListMain[i].addEventListener("mouseout", ListOut)
}

for (i = 0; i < clickToDetail.length; i++) {
    clickToDetail[i].addEventListener("click", selectList)
}

function ListOver() {
    if (!this.classList.contains("thisRoute")) {
        this.style.backgroundColor = "#FFF2CC"
        orderListMain[this.classList[1].substr(1)].style.backgroundColor = "#FFF2CC"
    }
}

function ListOut() {
    for (i = 0; i < orderListMain.length; i++) {
        if (!orderListMain[i].classList.contains("thisRoute")) {
            orderListMain[i].style.backgroundColor = "transparent"
        }
    }
}



function selectList() {
    let parms = new URLSearchParams(location.search)
    if (parms.has("search")) {
        location.href = `${THIS_URL}?type=${parms.get("type")}&search=${parms.get("search")}&id=${this.parentNode.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
    } else {
        location.href = `${THIS_URL}?id=${this.parentNode.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
    }
}

window.onload = function () {
    inputToDay()
    drawSchdule()
    DispatcBusFilter()
    // notPairFilter()
    addCommaList()

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
    if(params.has("id")){
        inputTextPrice.value = inputTextPrice.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        inputTextDriverAllowance.value = inputTextDriverAllowance.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}



let inputStartTime = ""
let inputEndTime = ""