const searchDate = document.querySelectorAll(".searchDate")
const dateControllBtn = document.querySelectorAll(".dateControllBtn")
const scheduleHeader = document.querySelector(".scheduleHeader")
const listHeader = document.querySelector(".orderListHeader span")
const inputTextquarter = document.querySelectorAll(".inputTextquarter")
const dateToday = document.querySelector(".dateToday")
const inputModules = document.querySelector(".inputModules")

// 날짜구하기
const toDay = new Date()
const year = toDay.getFullYear()
const month = toDay.getMonth() + 1
const date = toDay.getDate()
let controllDate = searchDate.value


// 기본 날짜
function inputToDay() {
    if (window.location.search.split("date1=")[1] == undefined) {
        for (i = 0; i < 2; i++) {
            if (month < 10) {
                if (date < 10) {
                    searchDate[i].value = `${year}-0${month}-0${date}`
                } else {
                    searchDate[i].value = `${year}-0${month}-${date}`
                }
            } else {
                if (date < 10) {
                    searchDate[i].value = `${year}-${month}-0${date}`
                } else {
                    searchDate[i].value = `${year}-${month}-${date}`
                }
            }
        }
    } else {
            searchDate[0].value = window.location.search.split("date1=")[1].substr(0, 10)
            searchDate[1].value = window.location.search.split("date2=")[1]
    }
    let week = ['일', '월', '화', '수', '목', '금', '토'];
    var dayOfWeek = week[new Date(searchDate[0].value).getDay()];
    if(params.get("id") == null){
        scheduleHeader.innerText = `${searchDate[0].value.substr(0, 4)}년 ${searchDate[0].value.substr(5, 2)}월 ${searchDate[0].value.substr(8, 2)}일 (${dayOfWeek})`
    }else{
        scheduleHeader.innerText = `${inputTextquarter[0].value.substr(0, 4)}년 ${inputTextquarter[0].value.substr(5, 2)}월 ${inputTextquarter[0].value.substr(8, 2)}일`
    }
    listHeader.innerText = `${searchDate[0].value.substr(0, 4)}년 ${searchDate[0].value.substr(5, 2)}월 ${searchDate[0].value.substr(8, 2)}일 (${dayOfWeek}) ~ ${searchDate[1].value.substr(0, 4)}년 ${searchDate[1].value.substr(5, 2)}월 ${searchDate[1].value.substr(8, 2)}일 (${dayOfWeek})`
}



// 날짜이동 "-"
dateControllBtn[0].addEventListener("click", dateToBefore)

function dateToBefore() {
    let pickDay = new Date(searchDate[0].value.substr(0, 4), searchDate[0].value.substr(5, 2) - 1, searchDate[0].value.substr(8, 2))

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
        location.href = `${window.location}?date1=${controllDate}&date2=${controllDate}`
    } else {
        location.href = `${location.href.split("date1=")[0]}date1=${controllDate}&date2=${controllDate}`
    }

}




// 날짜이동 "+"
dateControllBtn[1].addEventListener("click", dateTo)

function dateTo() {
    let pickDay = new Date(searchDate[0].value.substr(0, 4), searchDate[0].value.substr(5, 2) - 1, searchDate[0].value.substr(8, 2))

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
        location.href = `${window.location}?date1=${controllDate}&date2=${controllDate}`
    } else {
        location.href = `${location.href.split("date1=")[0]}date1=${controllDate}&date2=${controllDate}`
    }

}


// 날짜이동 "오늘"
dateToday.addEventListener("click", turnbackToday)

function turnbackToday(){
    location.href = `${window.location.href.split("?")[0]}`
}