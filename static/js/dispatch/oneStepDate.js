const searchDate = document.querySelector(".searchDate")
const dateControllBtn = document.querySelectorAll(".dateControllBtn")

// 날짜구하기
const toDay = new Date()
const year = toDay.getFullYear()
const month = toDay.getMonth() + 1
const date = toDay.getDate()


// 기본 날짜
window.onload = function () {
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
}


// 날짜이동 "-"
dateControllBtn[0].addEventListener("click", dateToBefore)

function dateToBefore() {
    let pickDay = new Date(searchDate.value.substr(0, 4), searchDate.value.substr(5, 2), searchDate.value.substr(8, 2) - 1)

    let pickYear = pickDay.getFullYear()
    let pickMonth = pickDay.getMonth()
    let pickDate = pickDay.getDate()

    if (pickDate == 31 && pickMonth == 2 || pickMonth == 4 || pickMonth == 6 || pickMonth == 9 || pickMonth == 11) {
        pickDate = new Date(pickYear, pickMonth, 0).getDate()
    }


    if (pickMonth < 10) {
        if (pickDate < 10) {
            searchDate.value = `${pickYear}-0${pickMonth}-0${pickDate}`
        } else {
            searchDate.value = `${pickYear}-0${pickMonth}-${pickDate}`
        }
    } else {
        if (pickDate < 10) {
            searchDate.value = `${pickYear}-${pickMonth}-0${pickDate}`
        } else {
            searchDate.value = `${pickYear}-${pickMonth}-${pickDate}`
        }
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
            searchDate.value = `${pickYear}-0${pickMonth}-0${pickDate}`
        } else {
            searchDate.value = `${pickYear}-0${pickMonth}-${pickDate}`
        }
    } else {
        if (pickDate < 10) {
            searchDate.value = `${pickYear}-${pickMonth}-0${pickDate}`
        } else {
            searchDate.value = `${pickYear}-${pickMonth}-${pickDate}`
        }
    }
}