const clickRoute = document.querySelectorAll(".listTableScroll .ListTableBox tr")
const orderListMain = document.querySelectorAll(".orderListMain .orderListScrollBox .orderListItem")
const orderListSub = document.querySelectorAll(".orderListSub .orderListScrollBox .orderListItem")

function thisRoute() {
    let parms = new URLSearchParams(location.search)    
    for (i = 0; i < orderListMain.length; i++) {
        if (orderListMain[i].classList[2] == parms.get("id")) {
            orderListMain[i].classList.add("thisRoute")
            orderListSub[i].classList.add("thisRoute")
        }
    }
}

for (i = 0; i < orderListMain.length; i++) {
    orderListMain[i].addEventListener("mouseover", ListOver)
    orderListMain[i].addEventListener("mouseout", ListOut)
    orderListMain[i].addEventListener("click", selectList)
    orderListSub[i].addEventListener("mouseover", ListOver)
    orderListSub[i].addEventListener("mouseout", ListOut)
    orderListSub[i].addEventListener("click", selectList)
}

function ListOver() {
    if (!this.classList.contains("thisRoute")) {
        this.style.backgroundColor = "#FFF2CC"
        orderListMain[this.classList[1] - 1].style.backgroundColor = "#FFF2CC"
        orderListSub[this.classList[1] - 1].style.backgroundColor = "#FFF2CC"
    }
}

function ListOut() {
    for (i = 0; i < orderListMain.length; i++) {
        if (!orderListMain[i].classList.contains("thisRoute")) {
            orderListMain[i].style.backgroundColor = "transparent"
            orderListSub[i].style.backgroundColor = "transparent"
        }
    }
}



function selectList() {
    let parms = new URLSearchParams(location.search)
    if(parms.has("route")){
        location.href = `/dispatch/order?route=${parms.get("route")}&id=${this.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
    }else{
        location.href = `/dispatch/order?id=${this.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
    }
}