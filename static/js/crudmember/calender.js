const prevBtn = document.querySelector(".controllBtnCell div:nth-child(1)")
const nextBtn = document.querySelector(".controllBtnCell div:nth-child(2)")
const dateText = document.querySelector(".controllBox span")
const todayBtn = document.querySelector(".todayBtn")
const sendMonth = document.querySelector("#sendMonth")
const hiddenMonth = document.querySelector(".hiddenMonth")
const dateTItle = document.querySelector(".controllBox span")
const PopupDataArea = document.querySelector(".PopupDataArea")
const fakeInput = document.querySelector(".fakeInput")
const check1 = document.querySelector(".check1")
const check2 = document.querySelector(".check2")
const popupContainer = document.querySelectorAll(".popupContainer")
const sendToHiddenChecker = document.querySelector(".sendToHiddenChecker")
const fileDeletBtn = document.querySelectorAll(".fileDeletBtn")


let moveMonth = 0;
let moveYear = 0;
let defualtDate = new Date();
let fixedDate = new Date();
let fixedYear = fixedDate.getFullYear();
let fixedMonth = fixedDate.getMonth();

window.onload = () => {

    let date = new Date();
    let url = window.location.search
    let cutUrl = url.split('=');


    if (window.location.search == "") {
        createCalender(date);
    } else {
        if (cutUrl[1].substr(5,) == "10" || cutUrl[1].substr(5,) == "11" || cutUrl[1].substr(5,) == "12") {
            date.setMonth(cutUrl[1].substr(5,) - 1)
            date.setFullYear(cutUrl[1].substr(0, 4))
        } else {
            date.setMonth(cutUrl[1].substr(6,) - 1)
            date.setFullYear(cutUrl[1].substr(0, 4))
        }
        moveMonth = date.getMonth() - new Date().getMonth()
        moveYear = date.getFullYear() - new Date().getFullYear()
        createCalender(date);
    }


    const dispatchCellOrder = document.querySelectorAll(".dispatchCellOrder")
    const dispatchCellRegularly = document.querySelectorAll(".dispatchCellRegularly")
    const dispatchCellOrderCount = document.querySelectorAll(".dispatchCellOrder div:nth-child(2)")
    const dispatchCellRegularlyCount = document.querySelectorAll(".dispatchCellRegularly div:nth-child(2)")
    const orderLink = document.querySelectorAll(".orderLink")
    const regularlyLink = document.querySelectorAll(".regularlyLink")


    for (i = 0; i < totalBusCnt.length; i++) {
        let linkDate = i
        dispatchCellOrderCount[i].innerText = `${curBusCnt[i]}/${totalBusCnt[i]}`
        dispatchCellRegularlyCount[i].innerText = `${r_curBusCnt[i]}/${r_totalBusCnt[i]}`
        if (totalBusCnt[i] > curBusCnt[i]) {
            dispatchCellOrder[i].classList.add("dispatchCellInclude")
            let linkMonth = date.getMonth()
            if (String(linkMonth).length == 1) {
                linkMonth = `0${date.getMonth() + 1}`
            } else {
                linkMonth = date.getMonth() + 1
            }
            if (linkDate < 9) {
                linkDate = `0${i + 1}`
            } else {
                linkDate = i + 1
            }

            orderLink[i].href = `http://kingbuserp.link/dispatch/order?route=&customer=&start_date=${date.getFullYear()}-${linkMonth}-${linkDate}&end_date=${date.getFullYear()}-${linkMonth}-${linkDate}`
        }
        if (r_totalBusCnt[i] > r_curBusCnt[i]) {
            dispatchCellRegularly[i].classList.add("dispatchCellInclude")
            let linkMonth = date.getMonth()
            if (String(linkMonth).length == 1) {
                linkMonth = `0${date.getMonth() + 1}`
            } else {
                linkMonth = date.getMonth() + 1
            }
            if (linkDate < 9) {
                linkDate = `0${i + 1}`
            } else {
                linkDate = i + 1
            }
            regularlyLink[i].href = `http://kingbuserp.link/dispatch/regularly?group=&route=&date=${date.getFullYear()}-${linkMonth}-${linkDate}`
        }
    }
}

prevBtn.addEventListener('click', prevMonth)

function prevMonth() {
    moveMonth = moveMonth - 1;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    newDate = new Date(date.setFullYear(date.getFullYear() + moveYear))
    if (newDate.getMonth() == 0) {
        moveYear = moveYear - 1;
    }
    // createCalender(newDate);
    if (String(newDate.getMonth() + 1).length == 1) {
        hiddenMonth.value = `${newDate.getFullYear()}-0${newDate.getMonth() + 1}`
    } else {
        hiddenMonth.value = `${newDate.getFullYear()}-${newDate.getMonth() + 1}`
    }
    sendMonth.submit()
}

nextBtn.addEventListener('click', nextMonth)

function nextMonth() {
    moveMonth = moveMonth + 1;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    newDate = new Date(date.setFullYear(date.getFullYear() + moveYear))
    if (newDate.getMonth() == 0) {
        moveYear = moveYear + 1;
    }
    // createCalender(newDate);
    if (String(newDate.getMonth() + 1).length == 1) {
        hiddenMonth.value = `${newDate.getFullYear()}-0${newDate.getMonth() + 1}`
    } else {
        hiddenMonth.value = `${newDate.getFullYear()}-${newDate.getMonth() + 1}`
    }
    sendMonth.submit()
}

todayBtn.addEventListener('click', thisMonth)

function thisMonth() {
    moveMonth = 0;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    // createCalender(newDate);
    if (String(newDate.getMonth() + 1).length == 1) {
        hiddenMonth.value = `${newDate.getFullYear()}-0${newDate.getMonth() + 1}`
    } else {
        hiddenMonth.value = `${newDate.getFullYear()}-${newDate.getMonth() + 1}`
    }
    sendMonth.submit()
}




function createCalender(date) {

    let thisYear = date.getFullYear();
    let lastMonth = date.getMonth();
    let today = date.getDate();

    let lastDay = new Date(thisYear, lastMonth + 1, 0);
    let getLastDay = lastDay.getDate();

    let startDay = new Date(thisYear, lastMonth, 1);
    let getStartDay = startDay.getDay();

    let dayCount = 0;
    let beforeMonthDay = getLastDay - (getStartDay - 1);
    let afterMonthDay = 1;
    let bodyDummy = ""

    for (i = 0; i < getStartDay; i++) {
        bodyDummy += `<div class="dayBox othereMonth"><span>${beforeMonthDay}</span></div>`
        beforeMonthDay = beforeMonthDay + 1;
    }
    for (i = 0; i < getLastDay; i++) {
        if (dayCount + 1 == today && fixedYear == thisYear && fixedMonth == lastMonth) {
            bodyDummy += `<div class="dayBox"><div class="today">${dayCount + 1}</div>
                <div class="dayDataBox dayDataBoxToday">
                    <div class="iconDataBox">
                        <div class="vehicleAlarmLight" onclick="openAlarmPopup()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25.805" height="26.744" viewBox="0 0 25.805 26.744">
                            <path id="Icon_awesome-bell" data-name="Icon awesome-bell"
                            d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z"
                            transform="translate(10.258 0) rotate(30)" fill="#fff" />
                        </svg>
                        </div>
                        <div class="dispatchAlarm" onclick="openDispatchPopup(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="15.464" height="20.025" viewBox="0 0 15.464 20.025">
                            <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document"
                            d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z"
                            transform="translate(-6.75 -3.375)" fill="#fff" />
                        </svg>
                        </div>
                    </div>
                    <div class="dispatchDataBox">
                        <a href="" class="orderLink">
                            <div class="dispatchCell dispatchCellOrder">
                                <div>일반배차</div>
                                <div></div>
                            </div>
                        </a>
                        <a href="" class="regularlyLink">
                            <div class="dispatchCell dispatchCellRegularly">
                                <div>출/퇴근배차</div>
                                <div></div>
                            </div>
                        </a>
                    </div>
                </div>
            </div>`
        } else {
            bodyDummy += `<div class="dayBox"><span>${dayCount + 1}</span>
                <div class="dayDataBox">
                    <div class="iconDataBox">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" width="25.805" height="26.744" viewBox="0 0 25.805 26.744">
                            <path id="Icon_awesome-bell" data-name="Icon awesome-bell"
                            d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z"
                            transform="translate(10.258 0) rotate(30)" fill="#fff" />
                        </svg>
                        </div>
                        <div class="dispatchAlarm" onclick="openDispatchPopup(this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="15.464" height="20.025" viewBox="0 0 15.464 20.025">
                            <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document"
                            d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z"
                            transform="translate(-6.75 -3.375)" fill="#fff" />
                        </svg>
                        </div>
                    </div>
                    <div class="dispatchDataBox">
                    <a href="" class="orderLink">
                        <div class="dispatchCell dispatchCellOrder">
                            <div>일반배차</div>
                            <div></div>
                        </div>
                    </a>
                    <a href="" class="regularlyLink">
                        <div class="dispatchCell dispatchCellRegularly">
                            <div>출/퇴근배차</div>
                            <div></div>
                        </div>
                    </a>
                    </div>
                </div>
            </div>`
        }
        dayCount = dayCount + 1;
    }
    for (i = (getStartDay + dayCount); i < 42; i++) {
        bodyDummy += `<div class="dayBox othereMonth"><span>${afterMonthDay}</span></div>`
        afterMonthDay = afterMonthDay + 1;
    }

    document.querySelector(`.calenderCreteTbody`).innerHTML = bodyDummy;
    dateText.innerText = `${thisYear}년 ${lastMonth + 1}월`


    //배차지시서 확인
    const dispatchAlarm = document.querySelectorAll(".dispatchAlarm")

    for (i = 0; i < dispatchAlarm.length; i++) {
        if (name1[i] !== "" && name2[i] !== "") {
            dispatchAlarm[i].style.backgroundColor = "#707070"
        }
    }
}







/*보험/정비알림*/
const popupAreaModules = document.querySelector('.popupAreaModules')
const popupAreaModulesDispatch = document.querySelector('.popupAreaModulesDispatch')
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const poupCloseBtn = document.querySelector(".PopupBtnBox div")
const disptchPoupCloseBtn = document.querySelector(".PopupBtnBoxDispatch div")

function openAlarmPopup() {
    popupAreaModules.style.display = 'block';
    for (i = 0; i < alarm.length; i++) {
        const PopupDataBox = document.createElement('div');
        PopupDataBox.setAttribute("class", "PopupDataBox")
        for (j = 0; j < 3; j++) {
            const kinds = document.createTextNode("구분")
            const vehicle = document.createTextNode("차량")
            const date = document.createTextNode("기간")
            const end = document.createTextNode("만료일")
            const thisKinds = document.createTextNode(`${alarm[i].type}`)
            const thisVehicle = document.createTextNode(`${alarm[i].num}`)
            const thisDate = document.createTextNode(`${alarm[i].duration}`)
            const PopupDataCell = document.createElement('div');
            const PopupDataTitle = document.createElement('div');
            const PopupData = document.createElement('div');
            const alarmLink = document.createElement('a');
            PopupDataCell.setAttribute("class", "PopupDataCell")
            PopupDataTitle.setAttribute("class", "PopupDataTitle")
            PopupData.setAttribute("class", "PopupData")
            alarmLink.setAttribute("href", `http://kingbuserp.link/vehicle/mgmt?select=vehicle&search=${alarm[i].num}`)
            if (j == 0) {
                PopupDataTitle.appendChild(kinds)
                PopupData.appendChild(thisKinds)
            } else if (j == 1) {
                PopupDataTitle.appendChild(vehicle)
                PopupData.appendChild(thisVehicle)
            } else if (j == 2) {
                if (alarm[i].type == "보험") {
                    PopupDataTitle.appendChild(end)
                    PopupData.appendChild(thisDate)
                    alarmLink.appendChild(PopupData)
                } else {
                    PopupDataTitle.appendChild(date)
                    PopupData.appendChild(thisDate)
                    alarmLink.appendChild(PopupData)
                }
            }
            PopupDataCell.appendChild(PopupDataTitle)
            if (j !== 2) {
                PopupDataCell.appendChild(PopupData)
            } else {
                PopupDataCell.appendChild(alarmLink)
            }
            PopupDataBox.appendChild(PopupDataCell)
        }
        PopupDataArea.appendChild(PopupDataBox)
    }
}

for (i = 0; i < 2; i++) {
    popupBgModules[i].addEventListener('click', closePopup)
}
SidemenuUseClose.addEventListener('click', closePopup)
poupCloseBtn.addEventListener('click', closePopup)
disptchPoupCloseBtn.addEventListener('click', closePopup)

function closePopup() {
    popupAreaModules.style.display = 'none';
    popupAreaModulesDispatch.style.display = 'none';
}


//배차지시서
function openDispatchPopup(element) {
    popupAreaModulesDispatch.style.display = 'block';
    popupContainer.action = "/dispatch/calendar/create"
    if (dateTItle.innerText.substr(6, 2) == "10" || dateTItle.innerText.substr(6, 2) == "11" || dateTItle.innerText.substr(6, 2) == "12") {
        if (parseInt(element.parentNode.parentNode.parentNode.firstChild.innerText) < 10) {
            fakeInput.value = `${dateTItle.innerText.substr(0, 4)}-${dateTItle.innerText.substr(6, 2)}-0${element.parentNode.parentNode.parentNode.firstChild.innerText}`
        } else {
            fakeInput.value = `${dateTItle.innerText.substr(0, 4)}-${dateTItle.innerText.substr(6, 2)}-${element.parentNode.parentNode.parentNode.firstChild.innerText}`
        }
    } else {
        if (parseInt(element.parentNode.parentNode.parentNode.firstChild.innerText) < 10) {
            fakeInput.value = `${dateTItle.innerText.substr(0, 4)}-0${dateTItle.innerText.substr(6, 1)}-0${element.parentNode.parentNode.parentNode.firstChild.innerText}`
        } else {
            fakeInput.value = `${dateTItle.innerText.substr(0, 4)}-0${dateTItle.innerText.substr(6, 1)}-${element.parentNode.parentNode.parentNode.firstChild.innerText}`
        }

    }
    for (i = 0; i < name1.length; i++) {
        check1.innerText = `${name1[parseInt(element.parentNode.parentNode.parentNode.firstChild.innerText) - 1]}`
        check2.innerText = `${name2[parseInt(element.parentNode.parentNode.parentNode.firstChild.innerText) - 1]}`
    }
}

fileDeletBtn[0].addEventListener('click', deleteChecker1)
fileDeletBtn[1].addEventListener('click', deleteChecker2)


function deleteChecker1() {
    popupContainer[1].action = "/dispatch/calendar/delete/1"
    sendToHiddenChecker.value = fakeInput.value
    popupContainer[1].submit()
}
function deleteChecker2() {
    popupContainer[1].action = "/dispatch/calendar/delete/2"
    sendToHiddenChecker.value = fakeInput.value
    popupContainer[1].submit()
}