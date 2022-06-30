const prevBtn = document.querySelector(".controllBtnCell div:nth-child(1)")
const nextBtn = document.querySelector(".controllBtnCell div:nth-child(2)")
const dateText = document.querySelector(".controllBox span")
const todayBtn = document.querySelector(".todayBtn")

let moveMonth = 0;
let defualtDate = new Date();
let fixedDate = new Date();
let fixedYear = fixedDate.getFullYear();
let fixedMonth = fixedDate.getMonth();

window.onload = () => {
    let date = new Date();
    createCalender(date);
}

prevBtn.addEventListener('click', prevMonth)

function prevMonth() {
    moveMonth = moveMonth - 1;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    createCalender(newDate);
}

nextBtn.addEventListener('click', nextMonth)

function nextMonth() {
    moveMonth = moveMonth + 1;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    createCalender(newDate);
}

todayBtn.addEventListener('click', thisMonth)

function thisMonth() {
    moveMonth = 0;
    let date = new Date();
    let newDate = new Date(date.setMonth(date.getMonth() + moveMonth))
    createCalender(newDate);
}




function createCalender(date) {
    let thisYear = date.getFullYear();
    let lastMonth = date.getMonth();
    let today = date.getDate();

    let lastDay = new Date(thisYear, lastMonth, 0);
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
    for (i = 1; i < getLastDay; i++) {
        if (dayCount + 1 == today && fixedYear == thisYear && fixedMonth == lastMonth) {
            bodyDummy += `<div class="dayBox"><div class="today">${dayCount + 1}</div>
                <div class="dayDataBox">
                    <div class="iconDataBox">
                        <div class="vehicleAlarm" onclick="openAlarmPopup()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25.805" height="26.744" viewBox="0 0 25.805 26.744">
                            <path id="Icon_awesome-bell" data-name="Icon awesome-bell"
                            d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z"
                            transform="translate(10.258 0) rotate(30)" fill="#fff" />
                        </svg>
                        </div>
                        <div class="dispatchAlarm" onclick="openDispatchPopup()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="15.464" height="20.025" viewBox="0 0 15.464 20.025">
                            <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document"
                            d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z"
                            transform="translate(-6.75 -3.375)" fill="#fff" />
                        </svg>
                        </div>
                    </div>
                    <div class="dispatchDataBox">
                        <div class="dispatchCell">
                            <div>일반배차</div>
                            
                            <div>2/3</div>
                        </div>
                        <div class="dispatchCell">
                            <div>출/퇴근배차</div>
                            <div>7/8</div>
                        </div>
                    </div>
                </div>
            </div>`
        } else {
            bodyDummy += `<div class="dayBox"><span>${dayCount + 1}</span>
                <div class="dayDataBox">
                    <div class="iconDataBox">
                    <div class="vehicleAlarm" onclick="openAlarmPopup()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25.805" height="26.744" viewBox="0 0 25.805 26.744">
                            <path id="Icon_awesome-bell" data-name="Icon awesome-bell"
                            d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z"
                            transform="translate(10.258 0) rotate(30)" fill="#fff" />
                        </svg>
                        </div>
                        <div class="dispatchAlarm" onclick="openDispatchPopup()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="15.464" height="20.025" viewBox="0 0 15.464 20.025">
                            <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document"
                            d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z"
                            transform="translate(-6.75 -3.375)" fill="#fff" />
                        </svg>
                        </div>
                    </div>
                    <div class="dispatchDataBox">
                        <div class="dispatchCell">
                            <div>일반배차</div>
                            <div>2/3</div>
                        </div>
                        <div class="dispatchCell">
                            <div>출/퇴근배차</div>
                            <div>7/8</div>
                        </div>
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


function openDispatchPopup() {
    popupAreaModulesDispatch.style.display = 'block';
}










/*배차지시서*/