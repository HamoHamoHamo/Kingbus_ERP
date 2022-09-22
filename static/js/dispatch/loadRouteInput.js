const clickRoute = document.querySelectorAll(".listTableScroll .ListTableBox tr")
const orderListMain = document.querySelectorAll(".orderListMain .orderListScrollBox .orderListItem")
const orderListSub = document.querySelectorAll(".orderListSub .orderListScrollBox .orderListItem")

for (i = 0; i < orderListMain.length; i++) {
    orderListMain[i].addEventListener("mouseover", ListOver)
    orderListMain[i].addEventListener("mouseout", ListOut)
    orderListMain[i].addEventListener("click", selectList)
    orderListSub[i].addEventListener("mouseover", ListOver)
    orderListSub[i].addEventListener("mouseout", ListOut)
    orderListSub[i].addEventListener("click", selectList)
}

function ListOver() {
    this.style.backgroundColor = "#b5b5b5"
    orderListMain[this.classList[1] - 1].style.backgroundColor = "#b5b5b5"
    orderListSub[this.classList[1] - 1].style.backgroundColor = "#b5b5b5"
}

function ListOut() {
    for (i = 0; i < orderListMain.length; i++) {
        orderListMain[i].style.backgroundColor = "transparent"
        orderListSub[i].style.backgroundColor = "transparent"
    }
}



function selectList() {
    location.href = `/dispatch/order?id=${this.classList[2]}&date1=${searchDate[0].value}&date2=${searchDate[1].value}`
}