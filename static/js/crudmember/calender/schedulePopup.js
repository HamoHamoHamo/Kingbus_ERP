const schedulePopup = document.querySelector(".schedule_popup")
const scheduleHiddenDate = document.querySelector(".schedule_create_hidden")
const scheduleCrateBtn = document.querySelector(".create_btn")
const scheduleCrateInput = document.querySelector(".basic_input[name=content]")
const scheduleCrateForm = document.querySelector(".schedule_create_form")
const createScheduleTr = document.querySelector(".basic_table_scroll_box tbody")
const scheduleListCheckerAll = document.querySelector(".schedule_checkbox_all")
const scheduleListDelete = document.querySelector(".schedule_list_delete_btn")
const scheduleListForm = document.querySelector(".schedule_list_form")


// 일정팝업 열기
for (i = 0; i < scheduleCell.length - 1; i++){
    scheduleCell[i].addEventListener("click", schedulePopupFtn)
};

function schedulePopupFtn(e){
    e.stopPropagation()
    schedulePopup.style.display = "block"
    createScheduleTr.innerText = ""

    let selectDate = this.parentNode.parentNode.children[0].children[0].innerText
    if(selectDate <= 9){
        selectDate = `0${selectDate}`
    }
    scheduleHiddenDate.value = `${calenderDate.innerText.substr(0,4)}-${calenderDate.innerText.substr(6,2)}-${selectDate}`

    let listCnt = this.parentNode.parentNode.children[0].children[0].innerText - 1
    for (i = 0; i < scheduleList[listCnt].length; i++){
        const scheduleTableTr = document.createElement("tr")
        createScheduleTr.appendChild(scheduleTableTr)
        
        const scheduleTableTd1 = document.createElement("td")
        scheduleTableTr.appendChild(scheduleTableTd1)

        const scheduleTableCheckbox = document.createElement("input")
        scheduleTableCheckbox.setAttribute("type", "checkbox")
        scheduleTableCheckbox.setAttribute("class", "schedule_list_checker")
        scheduleTableCheckbox.setAttribute("name", "check")
        scheduleTableCheckbox.setAttribute("value", scheduleList[listCnt][i].id)
        scheduleTableTd1.appendChild(scheduleTableCheckbox)
        
        const scheduleTableTd2 = document.createElement("td")
        scheduleTableTd2.innerText = i+1
        scheduleTableTr.appendChild(scheduleTableTd2)
        
        const scheduleTableTd3 = document.createElement("td")
        scheduleTableTd3.innerText = scheduleList[listCnt][i].content
        scheduleTableTr.appendChild(scheduleTableTd3)
        
        const scheduleTableTd4 = document.createElement("td")
        scheduleTableTd4.innerText = scheduleList[listCnt][i].creator
        scheduleTableTr.appendChild(scheduleTableTd4)
        
        const scheduleTableTd5 = document.createElement("td")
        scheduleTableTd5.innerText = scheduleList[listCnt][i].date
        scheduleTableTr.appendChild(scheduleTableTd5)
    };


    //일정목록 선택
    const scheduleListChecker = document.querySelectorAll(".schedule_list_checker")
    const allChecker = scheduleListCheckerAll

    scheduleListCheckerAll.addEventListener("change", () => allCheckerFtn(allChecker, scheduleListChecker))

    for (i = 0; i < scheduleListChecker.length; i++){
        scheduleListChecker[i].addEventListener("change", () => checkerFtn(allChecker, scheduleListChecker))
    };


    // 일정목록 삭제
    scheduleListDelete.addEventListener("click", deleteScheduleList)

    function deleteScheduleList(){
        let deleteSelect = 0
        for (i = 0; i < scheduleListChecker.length; i++){
            if(scheduleListChecker[i].checked){
                deleteSelect++
            }
        };
        if(deleteSelect === 0){
            alert("삭제할 일정을 선택해 주세요")
        }else{
            scheduleListForm.submit()
        }
    }
}


// 일정등록
scheduleCrateBtn.addEventListener("click", createScheduleFtn)

function createScheduleFtn(){
    if(scheduleCrateInput.value === ""){
        return alert("등록할 일정을 입력해 주세요.")
    }else{
        scheduleCrateForm.submit()
    }
}