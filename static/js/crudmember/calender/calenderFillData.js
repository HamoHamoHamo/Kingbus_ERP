const normalSchedule = document.querySelectorAll(".calender_contants_box")
const regularlyCntCell = document.querySelectorAll(".regularly_cnt_cell")
const orderCntCell = document.querySelectorAll(".order_cnt_cell")
const scheduleCell = document.querySelectorAll(".calender_schedule_Cell")

function sceduleFill(){
    let parms = new URLSearchParams(location.search)
    if(!parms.has("chagne")){
        for (i = 0; i < normalSchedule.length - 1; i++){
            regularlyCntCell[i].children[1].innerText = `${r_curBusCnt[i]}/${r_totalBusCnt[i]}`
            orderCntCell[i].children[1].innerText = `${curBusCnt[i]}/${totalBusCnt[i]}`
            if(scheduleList[i] === ""){
                const emptySchedule = document.createElement("div")
                emptySchedule.setAttribute("class", "empty_schedule_cell")
                emptySchedule.innerText = "일정이 없습니다."
                scheduleCell[i].appendChild(emptySchedule)
            }else{
                for (j = 0; j < scheduleList[i].length; j++){
                    const sceduleItem = document.createElement("div")
                    sceduleItem.setAttribute("class", "schedule_cell_Item")
                    sceduleItem.innerText = scheduleCell[i][j]
                    scheduleCell[i][j].appendChild(sceduleItem)
                };
            }
        };
    }else{

    }
}

sceduleFill()