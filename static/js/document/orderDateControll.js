const searchDate = document.querySelectorAll(".searchDate")
const dateControllBtn = document.querySelectorAll(".dateControllBtn")
const dateToday = document.querySelector(".dateToday")
const inputModules = document.querySelectorAll(".inputModules")



// 날짜이동 "-"
dateControllBtn[0].addEventListener("click", dateToBefore)

function dateToBefore() {
    let pickDay = new Date(inputModules[0].value.substr(0, 4), inputModules[0].value.substr(5, 2) - 1, inputModules[0].value.substr(8, 2))

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
    let pickDay = new Date(inputModules[0].value.substr(0, 4), inputModules[0].value.substr(5, 2) - 1, inputModules[0].value.substr(8, 2))

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