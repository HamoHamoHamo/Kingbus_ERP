const scheduleListCloseBtn = document.querySelector(".scheduleListCloseBtn")
const scheduleListTable = document.querySelector(".scheduleListForm tbody")
const checkboxAll = document.querySelector(".scheduleListForm thead input[type=checkbox]")


function openScheduleList() {
    popupAreaModules[3].style.display = "block"
    let targetSchedule = this.parentNode.parentNode.parentNode.children[0].children[0].innerText - 1
    for (i = 0; i < scheduleList[targetSchedule].length; i++) {
        const schedulTr = document.createElement("tr")
        schedulTr.setAttribute("class", "table-list_body-tr")
        scheduleListTable.appendChild(schedulTr)

        const scheduleCheckboxTd = document.createElement("td")
        scheduleCheckboxTd.setAttribute("class", "table-list_body-tr_td")
        schedulTr.appendChild(scheduleCheckboxTd)

        const scheduleCheckbox = document.createElement("input")
        scheduleCheckbox.setAttribute("type", "checkbox")
        scheduleCheckbox.setAttribute("name", "check")
        scheduleCheckbox.setAttribute("value", `${scheduleList[targetSchedule][i].id}`)
        scheduleCheckboxTd.appendChild(scheduleCheckbox)

        const scheduleNum = document.createElement("td")
        scheduleNum.setAttribute("class", "table-list_body-tr_td")
        scheduleNum.innerText = i + 1
        schedulTr.appendChild(scheduleNum)

        const scheduleContent = document.createElement("td")
        scheduleContent.setAttribute("class", "table-list_body-tr_td")
        scheduleContent.innerText = scheduleList[targetSchedule][i].content
        schedulTr.appendChild(scheduleContent)

        const scheduleCreator = document.createElement("td")
        scheduleCreator.setAttribute("class", "table-list_body-tr_td")
        scheduleCreator.innerText = scheduleList[targetSchedule][i].creator
        schedulTr.appendChild(scheduleCreator)

        const scheduleDate = document.createElement("td")
        scheduleDate.setAttribute("class", "table-list_body-tr_td")
        scheduleDate.innerText = scheduleList[targetSchedule][i].date
        schedulTr.appendChild(scheduleDate)
    };

    const checkbox = document.querySelectorAll("input[name=check]")

    checkboxAll.addEventListener("change", checkAll)

    function checkAll() {
        if (checkboxAll.checked) {
            for (i = 0; i < checkbox.length; i++) {
                checkbox[i].checked = true;
            };
        } else {
            for (i = 0; i < checkbox.length; i++) {
                checkbox[i].checked = false;
            };
        }
    }

    for (i = 0; i < checkbox.length; i++) {
        checkbox[i].addEventListener("change", checkOneToAll)
    };


    function checkOneToAll() {
        let checkCount = 0
        for (i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked) {
                checkCount++
            }
        }
        if (checkbox.length === checkCount) {
            checkboxAll.checked = true
        } else {
            checkboxAll.checked = false
        }
    }
}

popupBgModules[3].addEventListener("click", closeScheduleList)
SidemenuUseClose.addEventListener("click", closeScheduleList)
scheduleListCloseBtn.addEventListener("click", closeScheduleList)

function closeScheduleList() {
    popupAreaModules[3].style.display = "none"
}

function createSchaduleList() {
    let parms = new URLSearchParams(location.search)
    let beforeDayCount = 0
    if (!parms.has("change")) {
        for (i = 0; i < calenderDateBox.length; i++) {
            if (!calenderDateBox[i].classList.contains("beforeMonth") && !calenderDateBox[i].classList.contains("afterMonth")) {

                const dataCellCalender = calenderDateBox[i].querySelector(".dataCellCalender")

                for (j = 0; j < scheduleList[i - beforeDayCount].length; j++) {
                    if (j <= 2) {
                        const createSchdule = document.createElement("div")
                        createSchdule.setAttribute("class", "calnderItem")
                        createSchdule.innerText = scheduleList[i - beforeDayCount][j].content
                        dataCellCalender.appendChild(createSchdule)
                    } else {
                        const createSchduleMore = document.createElement("div")
                        createSchduleMore.setAttribute("class", "moreCalender")
                        createSchduleMore.innerText = `+${Object.keys(scheduleList[i - beforeDayCount]).length - 3}`
                        dataCellCalender.appendChild(createSchduleMore)
                        return
                    }
                }

            } else if (calenderDateBox[i].classList.contains("beforeMonth")) {
                beforeDayCount++
            }
        };
    }
}

createSchaduleList()