const clickRoute = document.querySelectorAll(".listTableScroll .ListTableBox tr")
const orderListMain = document.querySelectorAll(".orderListMain .orderListScrollBox .orderListItem")
const orderListSub = document.querySelectorAll(".orderListSub .orderListScrollBox .orderListItem")

function thisRoute() {
    for (i = 0; i < orderListMain.length; i++) {
        if (orderListMain[i].classList[2] == window.location.search.split("&")[0].substr(4,)) {
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
        this.style.backgroundColor = "#29b68b"
        orderListMain[this.classList[1] - 1].style.backgroundColor = "#29b68b"
        orderListSub[this.classList[1] - 1].style.backgroundColor = "#29b68b"
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
    location.href = `/dispatch/order?id=${this.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
}