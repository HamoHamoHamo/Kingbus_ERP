const pageTitleYear = document.querySelector(".pageTitle span:nth-child(1)")
const pageTitleMonth = document.querySelector(".pageTitle span:nth-child(2)")
const pageTitleDate = document.querySelector(".pageTitle span:nth-child(3)")
const pageTitleWeek = document.querySelector(".pageTitle span:nth-child(4)")
const printSizeCss = document.querySelector("#printSizeCss")

let getUrlYear = window.location.search.substr(6, 4)
let getUrlMonth = window.location.search.substr(11, 2)
let getUrlDate = window.location.search.substr(14, 2)
let Week = ['일', '월', '화', '수', '목', '금', '토']
let toDatYear = window.location.search.substr(6, 4)
let toDatMonth = ""
if (getUrlMonth == "11" || getUrlMonth == "12") {
    toDatMonth = parseInt(getUrlMonth) - 1
} else if (getUrlMonth == "10") {
    toDatMonth = 9
} else {
    toDatMonth = parseInt(getUrlMonth.substr(1,)) - 1
}
let toDatDate = ""
if (getUrlDate == "01" || getUrlDate == "02" || getUrlDate == "03" || getUrlDate == "04" || getUrlDate == "05" || getUrlDate == "06" || getUrlDate == "07" || getUrlDate == "08" || getUrlDate == "09") {
    toDatDate = parseInt(getUrlDate.substr(1,))
} else {
    toDatDate = getUrlDate
}
let toDay = Week[new Date(toDatYear, toDatMonth, toDatDate).getDay()]

window.onload = function () {
    pageTitleYear.innerText = `${getUrlYear}년`
    if (getUrlMonth == "10" || getUrlMonth == "11" || getUrlMonth == "12") {
        pageTitleMonth.innerText = `${getUrlMonth}월`
    } else {
        pageTitleMonth.innerText = `${getUrlMonth.substr(1,)}월`
    }
    if (getUrlDate == "01" || getUrlDate == "02" || getUrlDate == "03" || getUrlDate == "04" || getUrlDate == "05" || getUrlDate == "06" || getUrlDate == "07" || getUrlDate == "08" || getUrlDate == "09") {
        pageTitleDate.innerText = `${getUrlDate.substr(1,)}일`
    } else {
        pageTitleDate.innerText = `${getUrlDate}일`
    }
    // pageTitleWeek.innerText = `(${toDay})`
    // console.log(printSizeCss)
    // if(window.location.search.substr(22,2) == "A4"){
    //     printSizeCss.href = "../../../static/css/dispatch/printA4.css"
    // }else{
    //     printSizeCss.href = "../../../static/css/dispatch/printA3.css"
    // }
}
