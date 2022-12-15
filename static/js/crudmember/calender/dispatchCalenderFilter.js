const orderCalenderSearch = document.querySelector(".ordre_calender_search")
const orderCalenderSearchBtn = document.querySelector(".ordre_calender_search_btn")

orderCalenderSearchBtn.addEventListener("click", orderScheduleFilter)

function orderScheduleFilter(){
    for (i = 0; i < calenderOrderBox.length; i++){
        calenderOrderCell[i].innerText = ""
        calenderOrderTotalCnt[i].innerText = ""
    };    
    sceduleFill(orderCalenderSearch.value)
}

document.addEventListener("keydown", saveKeyPress)

function saveKeyPress(e) {
    if (e.keyCode === 13) {
        for (i = 0; i < calenderOrderBox.length; i++){
            calenderOrderCell[i].innerText = ""
            calenderOrderTotalCnt[i].innerText = ""
        };
        sceduleFill(orderCalenderSearch.value)
    }
}