const scheduleDriver = document.querySelectorAll('.tdDriver')
const popupAreaModules = document.querySelector('.popupAreaModules')
const popupBgModules = document.querySelector(".popupBgModules")
const popupBgModules2 = document.querySelector(".popupBgModules2")
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
        const newTdCheck4 = document.createElement('td');

        
        const newTextType = document.createTextNode(`${curData.work_type}`);
        const newTextTimeDepartureAll = document.createTextNode(`${curData.departure_date}~`);
        const newTextTimeArrivalAll = document.createTextNode(`${curData.arrival_date}`);
        const newTextTimeDeparture = document.createTextNode(`${curData.departure_date.substr(11,)}~`);
        const newTextTimeArrival = document.createTextNode(`${curData.arrival_date.substr(11,)}`);
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
        newTr.appendChild(newTdCheck4);

        
        popupListBox.appendChild(newTr);
    }
}

const popupAreaModules2 = document.querySelector('.popupAreaModules2');
const closeBtn = document.querySelector('.btncloseModules');
const popupRouteStatusTbody = document.querySelector('.popupRouteStatusTbody')
const stationTr = document.querySelector('#stationTr')

function addMinutes(time, minutesToAdd) {
    // 문자열을 분리하여 시와 분을 숫자로 변환
    const [hours, minutes] = time.split(':').map(Number);

    // 새로운 Date 객체 생성 (날짜는 중요하지 않으므로 임의 설정)
    const date = new Date();
    date.setHours(hours);
    date.setMinutes(minutes);

    // 분 추가 (음수면 빼는 효과)
    date.setMinutes(date.getMinutes() + minutesToAdd);

    // 결과를 %H:%M 형식으로 반환
    const newHours = String(date.getHours()).padStart(2, '0');
    const newMinutes = String(date.getMinutes()).padStart(2, '0');

    return `${newHours}:${newMinutes}`;
}

// 노선 팝업
function openScheduleDetail2() {
    popupAreaModules2.style.display = 'block';

    // 생성된 정류장 tr 삭제
    document.querySelectorAll('.tempTr').forEach(element => element.remove())
    console.log("CLASS", this.classList[0].split('/'))
    const id = this.classList[0].split('/')[0]
    const workType = this.classList[0].split('/')[1]

    getRouteStatusData(id, workType)

}

const createDatas = (datas) => {
    console.log("datas", datas)

    // 운행 노선 정보
    const routeName = document.querySelector('.routeName2')
    const driverName = document.querySelector('.driverName2')
    const vehicleNum = document.querySelector('.vehicleNum2')
    const driverPhone = document.querySelector('.driverPhone2')
    routeName.textContent = datas.connect.route
    driverName.textContent = datas.connect.name
    vehicleNum.textContent = datas.connect.vehicle_num
    driverPhone.textContent = datas.connect.phone
    

    // 운행 현황
    // 현황
    popupRouteStatusTbody.children[0].children[2].textContent = datas['wake_time'] ? "완료" : ""
    popupRouteStatusTbody.children[1].children[2].textContent = datas['drive_time'] ? "완료" : ""
    popupRouteStatusTbody.children[2].children[2].textContent = datas['departure_time'] ? "완료" : ""
    popupRouteStatusTbody.children[3].children[2].textContent = datas['drive_start_time'] ? "완료" : ""
    popupRouteStatusTbody.children[4].children[2].textContent = datas['driving_history'] ? "완료" : ""
    popupRouteStatusTbody.children[5].children[2].textContent = datas['drive_end_time'] ? "완료" : ""
    
    if (datas['wake_time_has_issue']) popupRouteStatusTbody.children[0].children[2].textContent = "문제 발생"
    if (datas['drive_time_has_issue']) popupRouteStatusTbody.children[1].children[2].textContent = "문제 발생"
    if (datas['departure_time_has_issue']) popupRouteStatusTbody.children[2].children[2].textContent = "문제 발생"

    // 완료시간
    popupRouteStatusTbody.children[0].children[3].textContent = datas['wake_time']
    popupRouteStatusTbody.children[1].children[3].textContent = datas['drive_time']
    popupRouteStatusTbody.children[2].children[3].textContent = datas['departure_time']
    popupRouteStatusTbody.children[3].children[3].textContent = datas['drive_start_time']
    popupRouteStatusTbody.children[4].children[3].textContent = datas['driving_history_time']
    popupRouteStatusTbody.children[5].children[3].textContent = datas['drive_end_time']

    // 예상완료시간
    const departure_time = datas.connect.departure_time
    const arrival_time = datas.connect.arrival_time
    popupRouteStatusTbody.children[0].children[4].textContent = `${addMinutes(departure_time, -90)} ~ ${addMinutes(departure_time, -60)}`
    popupRouteStatusTbody.children[1].children[4].textContent = `${addMinutes(departure_time, -60)} ~ ${addMinutes(departure_time, -20)}`
    popupRouteStatusTbody.children[2].children[4].textContent = `${addMinutes(departure_time, -20)} ~ ${departure_time}`
    popupRouteStatusTbody.children[3].children[4].textContent = departure_time
    popupRouteStatusTbody.children[5].children[4].textContent = arrival_time
    // popupRouteStatusTbody.children[3].children[4].textContent = `${addMinutes(departure_time, -15)} ~ ${addMinutes(departure_time, 15)}`
    // popupRouteStatusTbody.children[5].children[4].textContent = `${addMinutes(arrival_time, -15)} ~ ${addMinutes(arrival_time, 15)}`


    // 정류장 tr 추가
    const STATION_INDEX = 4
    Array.from(popupRouteStatusTbody.children).forEach((tr, index) => {
        if (index < STATION_INDEX) return

        
        if (index == STATION_INDEX) {
            datas['station_list'].forEach((station, stationIndex) => {
                const arrival_time = datas['arrival_time_list'].find(item => item.station_id__index == station.index)
                const tr = document.createElement('tr')
                const stationTd0 = document.createElement('td');
                const stationTd1 = document.createElement('td');
                const stationTd2 = document.createElement('td');
                const stationTd3 = document.createElement('td');
                const stationTd4 = document.createElement('td');

                stationTd0.textContent = index + stationIndex + 1
                stationTd1.textContent = `${station.station__name}`
                stationTd2.textContent = arrival_time?.has_issue == false ? "완료" : ""
                if (arrival_time?.has_issue) stationTd2.textContent = "문제 발생"
                stationTd3.textContent = arrival_time?.arrival_time
                stationTd4.textContent = `${addMinutes(station.time, -15)} ~ ${addMinutes(station.time, +15)}`

                tr.appendChild(stationTd0)
                tr.appendChild(stationTd1)
                tr.appendChild(stationTd2)
                tr.appendChild(stationTd3)
                tr.appendChild(stationTd4)
                tr.setAttribute('class', "tempTr")
                popupRouteStatusTbody.insertBefore(tr, stationTr)
            })
        }

        tr.children[0].textContent = index + 1 + datas['station_list'].length
    })

    // 문제 발생 클래스 적용, progress 값 계산
    let count = 0
    Array.from(popupRouteStatusTbody.children).forEach(tr => {
        if (tr.children[2].textContent == "문제 발생") {
            tr.children[2].setAttribute("class", "notDone")
        } else {
            tr.children[2].setAttribute("class", "")
        }
        // 완료 개수 세기
        if (tr.children[2].textContent == "완료") {
            count += 1
        }
    })
    const progressPercent = Math.ceil(count / popupRouteStatusTbody.children.length * 100)
    console.log("PERCENT", progressPercent)
    progressBarInner.textContent = `${progressPercent}%`
    progressBarInner.style.width = `${progressPercent}%`
}


// 정류장 목록 불러오기
const getRouteStatusData = (connectId, workType) => {
    // 기존에 있던 데이터 다 삭제
    // console.log("BACk")
    // popupRouteStatusTbody.replaceWith(backupTbody.cloneNode(true))
    
    console.log("TST", connectId, workType)
    const searchData = {
        'id' : connectId,
        'work_type': workType,
    }
    $.ajax({
        url: ROUTE_STATUS_URL,
        datatype: 'json',
        data: searchData,
        success: function (data) {
            // console.log(data);
            if (data.result == true) {
                createDatas(data.data)
                return
            } else {
                alert("에러가 발생했습니다.");
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}


popupBgModules.addEventListener('click', closePopup)
popupBgModules2.addEventListener('click', closePopup)
SidemenuUseClose.addEventListener('click', closePopup)
popupCloseBtn.addEventListener('click', closePopup)
closeBtn.addEventListener('click', closePopup)

function closePopup() {
    popupAreaModules.style.display = 'none'
    popupAreaModules2.style.display = 'none';
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
const LEFT_GAP = 16.46
window.onload = function () {
    for (i = 0; i < data.length; i++) {
        console.log(scheduleDriver[i].children[0].innerText);
        if (SELECT == "driver") {
            scheduleDriver[i].children[0].innerText = data[i][0].driver;
            scheduleDriver[i].children[1].innerText = data[i][0].driver_vehicle;
            scheduleDriver[i].children[2].innerText = data[i][0].driver_phone_num;
        } else if (SELECT == "vehicle") {
            scheduleDriver[i].children[0].innerText = data[i][0].bus;
            scheduleDriver[i].children[1].innerText = data[i][0].vehicle_driver;
            scheduleDriver[i].children[2].innerText = data[i][0].vehicle_driver_phone;
        }

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
            // 클래스에 id work_type 추가
            order.setAttribute("class", `${curData.id}/일반 orderLine`);
            order.setAttribute("title", `[${curData.bus} || ${startH}:${startM} ~ ${endH}:${endM} || ${curData.departure}▶${curData.arrival}`);

            if (curData.work_type == "일반") {
                if (curData.departure_date.substr(0, 10) == curData.arrival_date.substr(0, 10)) {
                    order.setAttribute("style", `left: ${((intStartH * 60 + intStartM) * 0.058) + LEFT_GAP}%; width: ${(((intEndH * 60 + intEndM) - (intStartH * 60 + intStartM)) * 0.058)}%;`);
                } else if (curData.departure_date.substr(0, 10) == dispatchDateFilter.value) {
                    order.setAttribute("style", `left: ${(((intStartH * 60 + intStartM) * 0.058)) - 0.1 + LEFT_GAP}%; width: ${100 - (((intStartH * 60 + intStartM) * 0.058)) - 16.38}%;`);
                } else if (curData.arrival_date.substr(0, 10) == dispatchDateFilter.value) {
                    order.setAttribute("style", `left: 0%; width: ${(((intEndH * 60 + intEndM) * 0.058)) - 0.1}%;`);
                } else {
                    order.setAttribute("style", `left: 0%; width: 83.52%;`);
                }
                if (curData.connect_check == '')
                {
                    order.style.border = '1px solid black';
                    order.style.backgroundColor = 'gray';
                }
                else if (curData.connect_check == '0')
                {
                    order.style.backgroundColor = 'red';
                    order.style.border = '1px solid black';
                }
                else if (curData.check == 'x') {
                    order.style.backgroundColor = 'red';
                }
                
                tr[i].appendChild(order);

                order.addEventListener('click', openScheduleDetail2)
            } else {
                const regularly = document.createElement('div');
                // 클래스에 id work_type 추가
                regularly.setAttribute("class", `${curData.id}/출퇴근 regularlyLine`);
                regularly.setAttribute("title", `[${curData.bus} || ${startH}:${startM} ~ ${endH}:${endM} || ${curData.departure}▶${curData.arrival}`);
                regularly.setAttribute("style", `left: ${((intStartH * 60 + intStartM) * 0.058) + LEFT_GAP}%; width: ${(((intEndH * 60 + intEndM) - (intStartH * 60 + intStartM)) * 0.058)}%;`);
                if (curData.connect_check == '')
                {
                    regularly.style.border = '1px solid black';
                    regularly.style.backgroundColor = 'gray';
                }
                else if (curData.connect_check == '0')
                {
                    regularly.style.backgroundColor = 'red';
                    regularly.style.border = '1px solid black';
                }
                else if (curData.check == 'x') {
                    regularly.style.backgroundColor = 'red';
                }
                
                tr[i].appendChild(regularly);

                regularly.addEventListener('click', openScheduleDetail2)
            }
        }
    }
}