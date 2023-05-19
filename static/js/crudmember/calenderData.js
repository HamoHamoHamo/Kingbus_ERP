function dataLoad() {

    let parms = new URLSearchParams(location.search)
    let beforeDayCount = 0
    if (!parms.has("change")) {
        for (i = 0; i < calenderDateBox.length; i++) {
            if (!calenderDateBox[i].classList.contains("beforeMonth") && !calenderDateBox[i].classList.contains("afterMonth")) {
                const regularlyData = calenderDateBox[i].querySelector(".regularlyData")
                regularlyData.innerText = `${r_curBusCnt[i - beforeDayCount]}/${r_totalBusCnt[i - beforeDayCount]}`
                if (r_curBusCnt[i - beforeDayCount] !== r_totalBusCnt[i - beforeDayCount]) {
                    regularlyData.classList.add("needDispatch")
                }
                regularlyData.parentNode.addEventListener("click", locationDispatch)
                const orderData = calenderDateBox[i].querySelector(".orderData")
                orderData.innerText = `${curBusCnt[i - beforeDayCount]}/${totalBusCnt[i - beforeDayCount]}`
                if (curBusCnt[i - beforeDayCount] !== totalBusCnt[i - beforeDayCount]) {
                    orderData.classList.add("needDispatch")
                }
                orderData.parentNode.addEventListener("click", locationDispatch)
            } else if (calenderDateBox[i].classList.contains("beforeMonth")) {
                beforeDayCount++
            }
        };
    }
}
if(AUTHORITY < 4){
    dataLoad()
}

function locationDispatch() {
    const date = new Date()
    let parms = new URLSearchParams(location.search)
    let dispatch = ""
    let dateUrl = ""
    let dispatchDate = this.parentNode.parentNode.parentNode.parentNode.children[0].children[0].innerText

    if (parms.has("year")) {
        if (dispatchDate < 10) {
            dateUrl = `${parms.get("year")}-${parms.get("month")}-0${dispatchDate}`
        } else {
            dateUrl = `${parms.get("year")}-${parms.get("month")}-${dispatchDate}`
        }
    } else {
        if (dispatchDate < 10) {
            dateUrl = `${nowYear}-${nowMonth}-0${dispatchDate}`
        } else {
            dateUrl = `${nowYear}-${nowMonth}-${dispatchDate}`
            console.log('testttt', dateUrl)
        }
    }
    console.log(dateUrl)

    if (this.children[1].classList.contains("regularlyData")) {
        dispatch = "regularly"
        location.href = `dispatch/regularly?group=&date=${dateUrl}`
    } else if (this.children[1].classList.contains("orderData")) {
        dispatch = "order"
        location.href = `dispatch/order?route=&date1=${dateUrl}&date2=${dateUrl}`
    }

}