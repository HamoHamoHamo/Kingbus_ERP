const getDate = document.querySelector(".FilterBox input")
const thisMonth = document.querySelector(".monthData .dashboardHeader")
const thisYear = document.querySelector(".yearData .dashboardHeader")

window.onload = function () {
    thisMonth.innerText = getDate.value.substr(5, 2) + "월 매출"
    thisYear.innerText = getDate.value.substr(0, 4) + "년 매출"
}