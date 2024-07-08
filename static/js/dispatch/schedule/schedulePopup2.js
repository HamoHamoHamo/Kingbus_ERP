const scheduleDriver = document.querySelectorAll('.tdDriver')
const popupAreaModules = document.querySelector('.popupAreaModules')
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelector(".PopupBtnBox div")
const driverName = document.querySelector(".driverName")
const vehicleNum = document.querySelector(".vehicleNum")
const driverPhone = document.querySelector(".driverPhone")
const dispatchDateFilter = document.querySelector(".dateFilterBox input")
const popupListBox = document.querySelector(".shcedulePopupTableBody tbody")
const tr = document.querySelectorAll(".tr")
const addTitle = document.querySelectorAll(".addTitle")


for (i = 0; i < scheduleDriver.length; i++) {
    scheduleDriver[i].addEventListener('click', openScheduleDetail)
}

const removeSpecial = /\(([^)]+)\)/;
function openScheduleDetail() {
    popupAreaModules.style.display = 'block'
    driverName.innerText = this.children[0].innerText
    vehicleNum.innerText = this.children[1].innerText
    driverPhone.innerText = this.children[2].innerText
    
    for (i = 0; i < data[this.childNodes[1].className].length; i++) {
        let curData = data[this.childNodes[1].className][i];
        let connectCheck = '';
        if (curData.connect_check == '1')
            connectCheck = '확인';
        else if (curData.connect_check == '0')
            connectCheck = '거부';

        const newTr = document.createElement('tr');
        const newTdType = document.createElement('td');
        const newTdBus = document.createElement('td');
        const newTdTime = document.createElement('td');
        const newTdRout = document.createElement('td');
        const newTdConnectCheck = document.createElement('td');
        const newTdCheck1 = document.createElement('td');
        const newTdCheck2 = document.createElement('td');
        const newTdCheck3 = document.createElement('td');
        
        const newTextType = document.createTextNode(`${curData.work_type}`);
        const newTextTimeDepartureAll = document.createTextNode(`${curData.departure_date}~`);
        const newTextTimeArrivalAll = document.createTextNode(`${curData.arrival_date}`);
        const newTextTimeDeparture = document.createTextNode(`${getHourAndMinuteWithColon(curData.empty_start_time)}~`);
        const newTextTimeArrival = document.createTextNode(`${getHourAndMinuteWithColon(curData.empty_end_time)}`);
        const newTextRoutDeparture = document.createTextNode(`${curData.departure}▶`);
        const newTextRoutArrival = document.createTextNode(`${curData.arrival}`);
        const newTextBus = document.createTextNode(curData.bus);
        const newTextConnectCheck = document.createTextNode(connectCheck);
        const newTextWakeT = document.createTextNode(curData.wake_t);
        const newTextDriveT = document.createTextNode(curData.drive_t);
        const newTextDepartureT = document.createTextNode(curData.departure_t);

        newTdType.appendChild(newTextType);
        if (curData.work_type == "일반") {
            newTdTime.appendChild(newTextTimeDepartureAll);
            newTdTime.appendChild(document.createElement('br'));
            newTdTime.appendChild(newTextTimeArrivalAll);
        } else {
            newTdTime.appendChild(newTextTimeDeparture);
            newTdTime.appendChild(newTextTimeArrival);
        }
        newTdRout.appendChild(newTextRoutDeparture);
        newTdRout.appendChild(document.createElement('br'));
        newTdRout.appendChild(newTextRoutArrival);
        newTdBus.appendChild(newTextBus);
        newTdConnectCheck.appendChild(newTextConnectCheck)
        newTdCheck1.appendChild(newTextWakeT);
        newTdCheck2.appendChild(newTextDriveT);
        newTdCheck3.appendChild(newTextDepartureT);

        newTr.appendChild(newTdType);
        newTr.appendChild(newTdBus);
        newTr.appendChild(newTdTime);
        newTr.appendChild(newTdRout);
        newTr.appendChild(newTdConnectCheck);
        newTr.appendChild(newTdCheck1);
        newTr.appendChild(newTdCheck2);
        newTr.appendChild(newTdCheck3);
        popupListBox.appendChild(newTr);
    }
}

popupBgModules.addEventListener('click', closePopup)
SidemenuUseClose.addEventListener('click', closePopup)
popupCloseBtn.addEventListener('click', closePopup)

function closePopup() {
    popupAreaModules.style.display = 'none'
    let removeCount = popupListBox.childNodes.length
    for (i = 0; i < removeCount; i++) {
        popupListBox.removeChild(popupListBox.firstChild)
    }
}

let startH = ""
let startM = ""
let endH = ""
let endM = ""
let curData = ""
let order = ""
let intStartH
let intStartM
let intEndH
let intEndM
window.onload = function () {
    for (i = 0; i < data.length; i++) {
        scheduleDriver[i].children[0].innerText = data[i][0].driver;
        scheduleDriver[i].children[1].innerText = data[i][0].driver_vehicle;
        scheduleDriver[i].children[2].innerText = data[i][0].driver_phone_num;

        for (j = 0; j < data[i].length; j++) {
            curData = data[i][j];
            order = document.createElement('div');
            startH = curData.departure_date.substr(11,).replace(/:/g, "").substr(0, 2);
            startM = curData.departure_date.substr(11,).replace(/:/g, "").substr(2,);
            endH = curData.arrival_date.substr(11,).replace(/:/g, "").substr(0, 2);
            endM = curData.arrival_date.substr(11,).replace(/:/g, "").substr(2,);
            intStartH = parseInt(startH);
            intStartM = parseInt(startM);
            intEndH = parseInt(endH);
            intEndM = parseInt(endM);
            let intStart = intStartH * 60 + intStartM
            let intEnd = intEndH * 60 + intEndM
            order.setAttribute("class", "orderLine");
            order.setAttribute("title", `[${curData.bus} || ${startH}:${startM} ~ ${endH}:${endM} || ${curData.departure}▶${curData.arrival}`);

            if (curData.work_type == "일반") {
                if (curData.departure_date.substr(0, 10) == curData.arrival_date.substr(0, 10)) {
                    order.setAttribute("style", `left: ${((intStart) * 0.058)}%; width: ${(((intEnd) - (intStart)) * 0.058)}%;`);
                } else if (curData.departure_date.substr(0, 10) == dispatchDateFilter.value) {
                    order.setAttribute("style", `left: ${(((intStart) * 0.058)) - 0.1}%; width: ${100 - (((intStart) * 0.058)) - 16.38}%;`);
                } else if (curData.arrival_date.substr(0, 10) == dispatchDateFilter.value) {
                    order.setAttribute("style", `left: 0%; width: ${(((intEnd) * 0.058)) - 0.1}%;`);
                } else {
                    order.setAttribute("style", `left: 0%; width: 83.52%;`);
                }
                if (curData.connect_check == '')
                {
                    // order.style.border = '1px solid black';
                    order.style.backgroundColor = 'gray';
                }
                else if (curData.connect_check == '0')
                {
                    order.style.backgroundColor = 'red';
                    // order.style.border = '1px solid black';
                }
                else if (curData.check == 'x') {
                    order.style.backgroundColor = 'red';
                }
                tr[i].appendChild(order);
            } else {
                
                // const regularly = document.createElement('div');
                // regularly.setAttribute("class", "regularlyLine");
                // regularly.setAttribute("title", `[${curData.bus} || ${startH}:${startM} ~ ${endH}:${endM} || ${curData.departure}▶${curData.arrival}`);
                // regularly.setAttribute("style", `left: ${((intStart) * 0.058)}%; width: ${(((intEnd) - (intStart)) * 0.058)}%;`);
                // if (curData.connect_check == '')
                // {
                //     regularly.style.border = '1px solid black';
                //     regularly.style.backgroundColor = 'gray';
                // }
                // else if (curData.connect_check == '0')
                // {
                //     regularly.style.backgroundColor = 'red';
                //     regularly.style.border = '1px solid black';
                // }
                // else if (curData.check == 'x') {
                //     regularly.style.backgroundColor = 'red';
                // }

                
                

                const timeList = curData.time_list.split(",")
                
                if (timeList.length >= 3) {
                    ({ hour: startH, minute: startM } = getHourAndMinute(curData['departure_time']));
                    ({ hour: endH, minute: endM } = getHourAndMinute(curData['arrival_time']));
                    intStart = parseInt(curData['departure_time'])
                    intEnd = parseInt(curData['arrival_time'])
                    createEmptyDrive(curData, tr[i])
                }

                const style = `left: ${((intStart) * 0.058)}%; width: ${(((intEnd) - (intStart)) * 0.058)}%; opacity: 50%;`
                const title = `[${curData.bus} || ${startH}:${startM} ~ ${endH}:${endM} || ${curData.departure}▶${curData.arrival}`
                tr[i].appendChild(createTimeTable(curData, title, style, '출퇴근'));
            }
        }
    }
}

function createEmptyDrive(curData,tr) {
    const { hour: intEndH, minute: intEndM } = getHourAndMinute(curData['departure_time'])
    const { hour: intStartH, minute: intStartM } = getHourAndMinute(curData['empty_start_time'])
    
    const startEmptyStyle = `left: ${((curData['empty_start_time']) * 0.058)}%; width: ${(((curData['departure_time']) - (curData['empty_start_time'])) * 0.058)}%; opacity: 50%; background-color: #c63dc6;`
    const startEmptyTitle = `[${curData.bus} || ${intStartH}:${intStartM} ~ ${intEndH}:${intEndM} || ${curData.departure}▶${curData.arrival}`
    tr.appendChild(createTimeTable(curData, startEmptyTitle, startEmptyStyle, '공차'))
    

    const { hour: intLastEmptyStartH, minute: intLastEmptyStartM } = getHourAndMinute(curData['arrival_time'])
    const { hour: intLastEmptyEndH, minute: intLastEmptyEndM } = getHourAndMinute(curData['empty_end_time'])

    const endEmptyStyle = `left: ${((curData['arrival_time']) * 0.058)}%; width: ${(((curData['empty_end_time']) - (curData['arrival_time'])) * 0.058)}%; opacity: 50%; background-color: #c63dc6;`
    const endEmptyTitle = `[${curData.bus} || ${intLastEmptyStartH}:${intLastEmptyStartM} ~ ${intLastEmptyEndH}:${intLastEmptyEndM} || ${curData.departure}▶${curData.arrival}`
    tr.appendChild(createTimeTable(curData, endEmptyTitle, endEmptyStyle, '공차'))
    
}

function createTimeTable(curData, title, style, type) {
    const div = document.createElement('div');
    div.setAttribute("class", "regularlyLine");
    div.setAttribute("title", title);
    div.setAttribute("style", style);
    
    if (type == '출퇴근') {
        if (curData.connect_check == '')
        {
            // div.style.border = '1px solid black';
            div.style.backgroundColor = 'gray';
        }
        else if (curData.connect_check == '0')
        {
            div.style.backgroundColor = 'red';
            // div.style.border = '1px solid black';
        }
        else if (curData.check == 'x') {
            div.style.backgroundColor = 'red';
        }
    } else if (type == '공차') {
        div.style.backgroundColor = 'purple';
    }
    return div
}

function getHourAndMinute(minutes) {
    return {
        hour : Math.floor(minutes / 60),
        minute : minutes % 60
    }
}

function getHourAndMinuteWithColon(minutes) {
    const formattedHours = String(Math.floor(minutes / 60)).padStart(2, '0');
    const formattedMinutes = String(minutes % 60).padStart(2, '0');


    return `${formattedHours}:${formattedMinutes}`
}