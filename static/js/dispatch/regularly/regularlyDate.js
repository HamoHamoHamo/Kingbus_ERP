const searchDate = document.querySelector(".searchDate")
const dateControllBtn = document.querySelectorAll(".dateControllBtn")
const scheduleHeader = document.querySelector(".scheduleHeader")
const dateToday = document.querySelector(".dateToday")

// 날짜구하기
const toDay = new Date()
const year = toDay.getFullYear()
const month = toDay.getMonth() + 1
const date = toDay.getDate()
let controllDate = searchDate.value


// 기본 날짜
function inputToDay() {
    if (window.location.search.split("date=")[1] == undefined) {
        if (month < 10) {
            if (date < 10) {
                searchDate.value = `${year}-0${month}-0${date}`
            } else {
                searchDate.value = `${year}-0${month}-${date}`
            }
        } else {
            if (date < 10) {
                searchDate.value = `${year}-${month}-0${date}`
            } else {
                searchDate.value = `${year}-${month}-${date}`
            }
        }
    } else {
        searchDate.value = window.location.search.split("date=")[1]
    }
    let week = ['일', '월', '화', '수', '목', '금', '토'];
    var dayOfWeek = week[new Date(searchDate.value).getDay()];
    scheduleHeader.innerText = `${searchDate.value.substr(0, 4)}년 ${searchDate.value.substr(5, 2)}월 ${searchDate.value.substr(8, 2)}일 (${dayOfWeek})`
}


// 날짜이동 "-"
dateControllBtn[0].addEventListener("click", dateToBefore)

function dateToBefore() {
    let pickDay = new Date(searchDate.value.substr(0, 4), searchDate.value.substr(5, 2) - 1, searchDate.value.substr(8, 2))

    pickDay.setDate(pickDay.getDate() - 1)

    let pickYear = pickDay.getFullYear()
    let pickMonth = pickDay.getMonth() + 1
    let pickDate = pickDay.getDate()

    if (pickMonth < 10) {
        if (pickDate < 10) {
            controllDate = `${pickYear}-0${pickMonth}-0${pickDate}`
        } else {
            controllDate = `${pickYear}-0${pickMonth}-${pickDate}`
        }
    } else {
        if (pickDate < 10) {
            controllDate = `${pickYear}-${pickMonth}-0${pickDate}`
        } else {
            controllDate = `${pickYear}-${pickMonth}-${pickDate}`
        }
    }



    if (!window.location.search) {
        location.href = `${window.location}?date=${controllDate}`
    } else if (window.location.search.split("date=")[0] == "?") {
        location.href = `${location.href.split("date=")[0]}date=${controllDate}`
    } else if (window.location.search.split("date=")[0].slice(-1) == "&") {
        location.href = `${location.href.split("date=")[0]}date=${controllDate}`
    } else {
        location.href = `${location.href}&date=${controllDate}`
    }

}




// 날짜이동 "+"
dateControllBtn[1].addEventListener("click", dateTo)

function dateTo() {
    let pickDay = new Date(searchDate.value.substr(0, 4), searchDate.value.substr(5, 2) - 1, searchDate.value.substr(8, 2))

    pickDay.setDate(pickDay.getDate() + 1)

    let pickYear = pickDay.getFullYear()
    let pickMonth = pickDay.getMonth() + 1
    let pickDate = pickDay.getDate()

    if (pickMonth < 10) {
        if (pickDate < 10) {
            controllDate = `${pickYear}-0${pickMonth}-0${pickDate}`
        } else {
            controllDate = `${pickYear}-0${pickMonth}-${pickDate}`
        }
    } else {
        if (pickDate < 10) {
            controllDate = `${pickYear}-${pickMonth}-0${pickDate}`
        } else {
            controllDate = `${pickYear}-${pickMonth}-${pickDate}`
        }
    }



    if (!window.location.search) {
        location.href = `${window.location}?date=${controllDate}`
    } else if (window.location.search.split("date=")[0] == "?") {
        location.href = `${location.href.split("date=")[0]}date=${controllDate}`
    } else if (window.location.search.split("date=")[0].slice(-1) == "&") {
        location.href = `${location.href.split("date=")[0]}date=${controllDate}`
    } else {
        location.href = `${location.href}&date=${controllDate}`
    }

}

// 날짜이동 "오늘"
dateToday.addEventListener("click", turnbackToday)

function turnbackToday(){
    let parms = new URLSearchParams(location.search)
    if(parms.has("group")){
        let groupUrl = window.location.search.split("group=")[1].split("&")[0]
        location.href = `${window.location.href.split("?")[0]}?group=${groupUrl}`
    }else{
        location.href = window.location.href.split("?")[0]
    }
}