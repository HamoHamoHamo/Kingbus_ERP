const prevBtn = document.querySelector(".controllBtnCell div:nth-child(1)")
const nextBtn = document.querySelector(".controllBtnCell div:nth-child(2)")
const dateText = document.querySelector(".controllBox span")
const todayBtn = document.querySelector(".todayBtn")
const sendMonth = document.querySelector("#sendMonth")
const hiddenMonth = document.querySelector(".hiddenMonth")
const dateTItle = document.querySelector(".controllBox span")
const PopupDataArea = document.querySelector(".PopupDataArea")
const fakeinput= document.querySelector(".fakeInput")
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
    const dispatchCellOrderCount = document.querySelectorAll(".dispatchCellOrder .dispatchCellCount")
    const dispatchCellRegularlyCount = document.querySelectorAll(".dispatchCellRegularly .dispatchCellCount")
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
            orderLink[i].href = `http://kingbuserp.link/dispatch/order?route=&customer=&date1=${date.getFullYear()}-${linkMonth}-${linkDate}&date2=${date.getFullYear()}-${linkMonth}-${linkDate}`
        } else {
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
            orderLink[i].href = `http://kingbuserp.link/dispatch/order?route=&customer=&date1=${date.getFullYear()}-${linkMonth}-${linkDate}&date2=${date.getFullYear()}-${linkMonth}-${linkDate}`
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
        } else {
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
            bodyDummy += 
            `<div class="dayBox">
            <div class="dateAndAlarmBox">
                <div class="claenderDate today">${dayCount + 1}</div>
                <div class="dispatchAlarm" onclick="openDispatchPopup(this)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16.464" height="21.025" viewBox="0 0 16.464 21.025">
                        <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document" d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z" transform="translate(-6.25 -2.875)" fill="#fff" stroke="#000" stroke-width="1"/>
                    </svg>
                </div>
                <div class="vehicleAlarmLight" onclick="openAlarmPopup()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25.805" height="26.744" viewBox="0 0 25.805 26.744">
                        <path id="Icon_awesome-bell" data-name="Icon awesome-bell" d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z" transform="translate(10.258) rotate(30)" fill="#fff"/>
                    </svg>
                </div>
            </div>
            <a href="" class="regularlyLink">
                <div class="dispatchCell dispatchCellRegularly">
                    <div class="dispatchCellTop">
                        <div class="dispatchCellIcon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="37.312" height="30.012" viewBox="0 0 37.312 30.012">
                                <g id="그룹_1460" data-name="그룹 1460" transform="translate(5784.5 16541)">
                                <g id="그룹_1383" data-name="그룹 1383" transform="translate(-5784.5 -16541)">
                                    <g id="패스_316" data-name="패스 316" transform="translate(0 4.056)" fill="none">
                                    <path d="M3.245,0H34.067a3.245,3.245,0,0,1,3.245,3.245V22.712a3.245,3.245,0,0,1-3.245,3.245H3.245A3.245,3.245,0,0,1,0,22.712V3.245A3.245,3.245,0,0,1,3.245,0Z" stroke="none"/>
                                    <path d="M 3.244514465332031 1 C 2.006881713867188 1 1.000003814697266 2.006879806518555 1.000003814697266 3.244510650634766 L 1.000003814697266 22.71157073974609 C 1.000003814697266 23.94919967651367 2.006881713867188 24.95608139038086 3.244514465332031 24.95608139038086 L 34.06735229492188 24.95608139038086 C 35.30498504638672 24.95608139038086 36.31186294555664 23.94919967651367 36.31186294555664 22.71157073974609 L 36.31186294555664 3.244510650634766 C 36.31186294555664 2.006879806518555 35.30498504638672 1 34.06735229492188 1 L 3.244514465332031 1 M 3.244514465332031 0 L 34.06735229492188 0 C 35.8592529296875 0 37.31186294555664 1.452610015869141 37.31186294555664 3.244510650634766 L 37.31186294555664 22.71157073974609 C 37.31186294555664 24.50345993041992 35.8592529296875 25.95608139038086 34.06735229492188 25.95608139038086 L 3.244514465332031 25.95608139038086 C 1.452613830566406 25.95608139038086 3.814697265625e-06 24.50345993041992 3.814697265625e-06 22.71157073974609 L 3.814697265625e-06 3.244510650634766 C 3.814697265625e-06 1.452610015869141 1.452613830566406 0 3.244514465332031 0 Z" stroke="none" fill="#000"/>
                                    </g>
                                    <g id="패스_313" data-name="패스 313" transform="translate(10.545 0)" fill="none">
                                    <path d="M1.622,0H14.6a1.622,1.622,0,0,1,1.622,1.622V4.158c0,.9-.726.9-1.622.9H1.622c-.9,0-1.622-.008-1.622-.9V1.622A1.622,1.622,0,0,1,1.622,0Z" stroke="none"/>
                                    <path d="M 1.622255325317383 1 C 1.279135704040527 1 0.999995231628418 1.279139995574951 0.999995231628418 1.622260093688965 L 0.999995231628418 4.044703006744385 C 1.179670333862305 4.062498569488525 1.444009780883789 4.0625 1.622255325317383 4.0625 L 14.60029602050781 4.0625 C 14.77854156494141 4.0625 15.04288101196289 4.062498569488525 15.22255611419678 4.044703006744385 L 15.22255611419678 1.622260093688965 C 15.22255611419678 1.279139995574951 14.94341564178467 1 14.60029602050781 1 L 1.622255325317383 1 M 1.622255325317383 0 L 14.60029602050781 0 C 15.49624538421631 0 16.22255516052246 0.7263097763061523 16.22255516052246 1.622260093688965 L 16.22255516052246 4.158200263977051 C 16.22255516052246 5.054150104522705 15.49624538421631 5.0625 14.60029602050781 5.0625 L 1.622255325317383 5.0625 C 0.7263059616088867 5.0625 -3.814697265625e-06 5.054150104522705 -3.814697265625e-06 4.158200263977051 L -3.814697265625e-06 1.622260093688965 C -3.814697265625e-06 0.7263097763061523 0.7263059616088867 0 1.622255325317383 0 Z" stroke="none" fill="#000"/>
                                    </g>
                                </g>
                                <path id="패스_314" data-name="패스 314" d="M0,0,13.685,6.1" transform="translate(-5783.689 -16530.455)" fill="none" stroke="#000" stroke-width="1"/>
                                <g id="사각형_11245" data-name="사각형 11245" transform="translate(-5770.711 -16527.211)" fill="none" stroke="#000" stroke-width="1">
                                    <rect width="9.734" height="6.489" rx="1" stroke="none"/>
                                    <rect x="0.5" y="0.5" width="8.734" height="5.489" rx="0.5" fill="none"/>
                                </g>
                                <path id="패스_315" data-name="패스 315" d="M13.666,6.309,27.388,0" transform="translate(-5775.388 -16530.455)" fill="none" stroke="#000" stroke-width="1"/>
                                </g>
                            </svg>
                        </div>
                        <div class="dispatchCellTitle">출/퇴근배차</div>
                    </div>
                    <div class="dispatchCellCount"></div>
                </div>
            </a>
            <a href="" class="orderLink">
                <div class="dispatchCell dispatchCellOrder">
                    <div class="dispatchCellTop">
                        <div class="dispatchCellIcon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="41.5" height="37.238" viewBox="0 0 41.5 37.238">
                                <path id="Icon_awesome-map-marked-alt" data-name="Icon awesome-map-marked-alt" d="M20.25,0a8.859,8.859,0,0,0-8.859,8.859c0,3.956,5.79,11.166,8.009,13.783a1.109,1.109,0,0,0,1.7,0c2.218-2.617,8.009-9.827,8.009-13.783A8.859,8.859,0,0,0,20.25,0Zm0,11.813A2.953,2.953,0,1,1,23.2,8.859,2.953,2.953,0,0,1,20.25,11.813ZM1.415,15.184A2.25,2.25,0,0,0,0,17.273v17.6a1.125,1.125,0,0,0,1.543,1.045L11.25,31.5V15.112a21.293,21.293,0,0,1-1.494-3.264ZM20.25,25.289A3.36,3.36,0,0,1,17.683,24.1C16.3,22.466,14.83,20.608,13.5,18.7V31.5L27,36V18.7c-1.33,1.9-2.8,3.763-4.183,5.394A3.361,3.361,0,0,1,20.25,25.289ZM38.957,11.332,29.25,15.75V36l9.835-3.934A2.25,2.25,0,0,0,40.5,29.977v-17.6A1.125,1.125,0,0,0,38.957,11.332Z" transform="translate(0.5 0.5)" fill="none" stroke="#000" stroke-width="1"/>
                            </svg>
                        </div>
                        <div class="dispatchCellTitle">일반배차</div>
                    </div>
                    <div class="dispatchCellCount"></div>
                </div>
            </a>
        </div>`
        } else {
            bodyDummy += 
            `<div class="dayBox">
            <div class="dateAndAlarmBox">
                <div class="claenderDate">${dayCount + 1}</div>
                <div class="dispatchAlarm" onclick="openDispatchPopup(this)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16.464" height="21.025" viewBox="0 0 16.464 21.025">
                        <path id="Icon_ionic-md-document" data-name="Icon ionic-md-document" d="M16.028,3.375H8.683A1.929,1.929,0,0,0,6.75,5.3V21.475A1.929,1.929,0,0,0,8.683,23.4h11.6a1.929,1.929,0,0,0,1.933-1.926V9.537Zm-.773,6.932V4.915l5.412,5.391Z" transform="translate(-6.25 -2.875)" fill="#fff" stroke="#000" stroke-width="1"/>
                    </svg>
                </div>
                <div class="vehicleAlarm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="27.171" height="28.111" viewBox="0 0 27.171 28.111">
                        <path id="Icon_awesome-bell" data-name="Icon awesome-bell" d="M8.976,20.517a2.564,2.564,0,0,0,2.563-2.565H6.413A2.564,2.564,0,0,0,8.976,20.517Zm8.631-6c-.774-.832-2.223-2.083-2.223-6.183a6.328,6.328,0,0,0-5.127-6.218V1.282a1.281,1.281,0,1,0-2.563,0v.835A6.328,6.328,0,0,0,2.568,8.335c0,4.1-1.449,5.351-2.223,6.183a1.252,1.252,0,0,0-.345.87A1.283,1.283,0,0,0,1.286,16.67H16.666a1.283,1.283,0,0,0,1.286-1.282A1.251,1.251,0,0,0,17.607,14.518Z" transform="translate(10.941 0.684) rotate(30)" fill="#fff" stroke="#000" stroke-width="1"/>
                    </svg>
                </div>
            </div>
            <a href="" class="regularlyLink">
                <div class="dispatchCell dispatchCellRegularly">
                    <div class="dispatchCellTop">
                        <div class="dispatchCellIcon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="37.312" height="30.012" viewBox="0 0 37.312 30.012">
                                <g id="그룹_1460" data-name="그룹 1460" transform="translate(5784.5 16541)">
                                <g id="그룹_1383" data-name="그룹 1383" transform="translate(-5784.5 -16541)">
                                    <g id="패스_316" data-name="패스 316" transform="translate(0 4.056)" fill="none">
                                    <path d="M3.245,0H34.067a3.245,3.245,0,0,1,3.245,3.245V22.712a3.245,3.245,0,0,1-3.245,3.245H3.245A3.245,3.245,0,0,1,0,22.712V3.245A3.245,3.245,0,0,1,3.245,0Z" stroke="none"/>
                                    <path d="M 3.244514465332031 1 C 2.006881713867188 1 1.000003814697266 2.006879806518555 1.000003814697266 3.244510650634766 L 1.000003814697266 22.71157073974609 C 1.000003814697266 23.94919967651367 2.006881713867188 24.95608139038086 3.244514465332031 24.95608139038086 L 34.06735229492188 24.95608139038086 C 35.30498504638672 24.95608139038086 36.31186294555664 23.94919967651367 36.31186294555664 22.71157073974609 L 36.31186294555664 3.244510650634766 C 36.31186294555664 2.006879806518555 35.30498504638672 1 34.06735229492188 1 L 3.244514465332031 1 M 3.244514465332031 0 L 34.06735229492188 0 C 35.8592529296875 0 37.31186294555664 1.452610015869141 37.31186294555664 3.244510650634766 L 37.31186294555664 22.71157073974609 C 37.31186294555664 24.50345993041992 35.8592529296875 25.95608139038086 34.06735229492188 25.95608139038086 L 3.244514465332031 25.95608139038086 C 1.452613830566406 25.95608139038086 3.814697265625e-06 24.50345993041992 3.814697265625e-06 22.71157073974609 L 3.814697265625e-06 3.244510650634766 C 3.814697265625e-06 1.452610015869141 1.452613830566406 0 3.244514465332031 0 Z" stroke="none" fill="#000"/>
                                    </g>
                                    <g id="패스_313" data-name="패스 313" transform="translate(10.545 0)" fill="none">
                                    <path d="M1.622,0H14.6a1.622,1.622,0,0,1,1.622,1.622V4.158c0,.9-.726.9-1.622.9H1.622c-.9,0-1.622-.008-1.622-.9V1.622A1.622,1.622,0,0,1,1.622,0Z" stroke="none"/>
                                    <path d="M 1.622255325317383 1 C 1.279135704040527 1 0.999995231628418 1.279139995574951 0.999995231628418 1.622260093688965 L 0.999995231628418 4.044703006744385 C 1.179670333862305 4.062498569488525 1.444009780883789 4.0625 1.622255325317383 4.0625 L 14.60029602050781 4.0625 C 14.77854156494141 4.0625 15.04288101196289 4.062498569488525 15.22255611419678 4.044703006744385 L 15.22255611419678 1.622260093688965 C 15.22255611419678 1.279139995574951 14.94341564178467 1 14.60029602050781 1 L 1.622255325317383 1 M 1.622255325317383 0 L 14.60029602050781 0 C 15.49624538421631 0 16.22255516052246 0.7263097763061523 16.22255516052246 1.622260093688965 L 16.22255516052246 4.158200263977051 C 16.22255516052246 5.054150104522705 15.49624538421631 5.0625 14.60029602050781 5.0625 L 1.622255325317383 5.0625 C 0.7263059616088867 5.0625 -3.814697265625e-06 5.054150104522705 -3.814697265625e-06 4.158200263977051 L -3.814697265625e-06 1.622260093688965 C -3.814697265625e-06 0.7263097763061523 0.7263059616088867 0 1.622255325317383 0 Z" stroke="none" fill="#000"/>
                                    </g>
                                </g>
                                <path id="패스_314" data-name="패스 314" d="M0,0,13.685,6.1" transform="translate(-5783.689 -16530.455)" fill="none" stroke="#000" stroke-width="1"/>
                                <g id="사각형_11245" data-name="사각형 11245" transform="translate(-5770.711 -16527.211)" fill="none" stroke="#000" stroke-width="1">
                                    <rect width="9.734" height="6.489" rx="1" stroke="none"/>
                                    <rect x="0.5" y="0.5" width="8.734" height="5.489" rx="0.5" fill="none"/>
                                </g>
                                <path id="패스_315" data-name="패스 315" d="M13.666,6.309,27.388,0" transform="translate(-5775.388 -16530.455)" fill="none" stroke="#000" stroke-width="1"/>
                                </g>
                            </svg>
                        </div>
                        <div class="dispatchCellTitle">출/퇴근배차</div>
                    </div>
                    <div class="dispatchCellCount"></div>
                </div>
            </a>
            <a href="" class="orderLink">
                <div class="dispatchCell dispatchCellOrder">
                    <div class="dispatchCellTop">
                        <div class="dispatchCellIcon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="41.5" height="37.238" viewBox="0 0 41.5 37.238">
                                <path id="Icon_awesome-map-marked-alt" data-name="Icon awesome-map-marked-alt" d="M20.25,0a8.859,8.859,0,0,0-8.859,8.859c0,3.956,5.79,11.166,8.009,13.783a1.109,1.109,0,0,0,1.7,0c2.218-2.617,8.009-9.827,8.009-13.783A8.859,8.859,0,0,0,20.25,0Zm0,11.813A2.953,2.953,0,1,1,23.2,8.859,2.953,2.953,0,0,1,20.25,11.813ZM1.415,15.184A2.25,2.25,0,0,0,0,17.273v17.6a1.125,1.125,0,0,0,1.543,1.045L11.25,31.5V15.112a21.293,21.293,0,0,1-1.494-3.264ZM20.25,25.289A3.36,3.36,0,0,1,17.683,24.1C16.3,22.466,14.83,20.608,13.5,18.7V31.5L27,36V18.7c-1.33,1.9-2.8,3.763-4.183,5.394A3.361,3.361,0,0,1,20.25,25.289ZM38.957,11.332,29.25,15.75V36l9.835-3.934A2.25,2.25,0,0,0,40.5,29.977v-17.6A1.125,1.125,0,0,0,38.957,11.332Z" transform="translate(0.5 0.5)" fill="none" stroke="#000" stroke-width="1"/>
                            </svg>
                        </div>
                        <div class="dispatchCellTitle">일반배차</div>
                    </div>
                    <div class="dispatchCellCount"></div>
                </div>
            </a>
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