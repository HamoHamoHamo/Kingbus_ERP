const normalSchedule = document.querySelectorAll(".calender_contants_box")
const regularlyCntCell = document.querySelectorAll(".regularly_cnt_cell")
const orderCntCell = document.querySelectorAll(".order_cnt_cell")
const scheduleCell = document.querySelectorAll(".calender_schedule_Cell")
const dispatchCheckIcon = document.querySelectorAll(".dispatch_check")
const calenderOrderBox = document.querySelectorAll(".calender_order_box")
const calenderOrderCell = document.querySelectorAll(".calender_order_cell")
const calenderOrderTotalCnt = document.querySelectorAll(".calender_order_total_cnt")

function sceduleFill(filter) {
    let parms = new URLSearchParams(location.search)
    if (!parms.has("change")) {
        for (i = 0; i < normalSchedule.length - 1; i++) {

            // 배차확인 정보
            if (checkList[i] !== "") {
                dispatchCheckIcon[i].children[0].children[0].style.fill = "#61B4E5"
            }

            // 출·퇴근 배차정보
            regularlyCntCell[i].children[1].innerText = `${r_curBusCnt[i]}/${r_totalBusCnt[i]}`

            // 일반 배차정보
            orderCntCell[i].children[1].innerText = `${curBusCnt[i]}/${totalBusCnt[i]}`

            // 일정 정보
            if (scheduleList[i] === "") {
                const emptySchedule = document.createElement("div")
                emptySchedule.setAttribute("class", "empty_schedule_cell")
                emptySchedule.innerText = "일정이 없습니다."
                scheduleCell[i].appendChild(emptySchedule)
            } else {
                for (j = 0; j < scheduleList[i].length; j++) {
                    if (j < 3) {
                        const sceduleItem = document.createElement("div")
                        sceduleItem.setAttribute("class", "schedule_cell_Item")
                        if (Object.values(scheduleList[i][j])[0].length > 7) {
                            sceduleItem.innerText = `${Object.values(scheduleList[i][j])[0].substr(0, 6)}...`
                        } else {
                            sceduleItem.innerText = Object.values(scheduleList[i][j])[0]
                        }
                        scheduleCell[i].appendChild(sceduleItem)
                    } else if (j === 3) {
                        const sceduleItemCnt = document.createElement("div")
                        sceduleItemCnt.setAttribute("class", "schedule_cell_cnt_box")
                        sceduleItemCnt.innerText = "+1"
                        scheduleCell[i].appendChild(sceduleItemCnt)
                    } else {
                        scheduleCell[i].children[3].innerText = `+${j - 2}`
                    }
                };
            }
        };
    } else {
        for (i = 0; i < calenderOrderBox.length - 1; i++) {
            if (changeOrderList[i] !== "") {
                let totalCnt = 0
                for (j = 0; j < changeOrderList[i].length; j++) {
                    if(Object.values(changeOrderList[i][j])[0].includes(filter)){
                        const orderCell = document.createElement("div")
                        orderCell.setAttribute("class", "calender_order_item")
                        calenderOrderCell[i].appendChild(orderCell)
    
                        const orderCellContents = document.createElement("div")
                        orderCellContents.setAttribute("class", "calender_order_contets")
                        if (Object.values(changeOrderList[i][j])[0].length > 9) {
                            orderCellContents.innerText = `${Object.values(changeOrderList[i][j])[0].substr(0, 8)}...`
                        } else {
                            orderCellContents.innerText = Object.values(changeOrderList[i][j])[0]
                        }
                        orderCell.appendChild(orderCellContents)
    
                        const orderCellCnt = document.createElement("div")
                        orderCellCnt.setAttribute("class", "calender_order_cnt")
                        orderCellCnt.innerText = Object.values(changeOrderList[i][j])[1]
                        orderCell.appendChild(orderCellCnt)

                        totalCnt++
                    }
                };
                calenderOrderTotalCnt[i].innerText = totalCnt
            }else{
                calenderOrderTotalCnt[i].innerText = 0
            }
        }
    }
}

sceduleFill("")