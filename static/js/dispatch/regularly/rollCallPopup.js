import { addEventClosePopup, closePopup } from "/static/js/common/popupCommon.js"

addEventClosePopup()

const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const closeBtn = document.querySelectorAll(".btn-close")
Array.from(closeBtn).forEach(item => item.addEventListener("click", closePopup))

const routeStatusPopupBtn = document.querySelectorAll(".routeStatusPopupBtn")
const driverStatusPopupBtn = document.querySelectorAll(".driverStatusPopupBtn")
const progressBarInner = document.querySelector(".progress-bar-inner")



Array.from(routeStatusPopupBtn).forEach(item => item.addEventListener("click", openRouteStatusPopup))
Array.from(driverStatusPopupBtn).forEach(item => item.addEventListener("click", openDriverStatusPopup))


// 팝업 열기
function openRouteStatusPopup() {
    popupAreaModules[0].style.display = "block";
    const id = this.parentNode.classList[0]

    document.querySelectorAll('.tempTr').forEach(element => element.remove())
    getRouteStatusData(id)
}


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

const popupRouteStatusTbody = document.querySelector('.popupRouteStatusTbody')

const stationTr = document.querySelector('#stationTr')


const createDatas = (datas) => {
    console.log("datas", datas)

    // 운행 노선 정보
    const infoHeaders = [
        'route',
        'name',
        'vehicle_num',
        'phone',
    ]
    const routeName = document.querySelector('.routeName')
    const driverName = document.querySelector('.driverName')
    const vehicleNum = document.querySelector('.vehicleNum')
    const driverPhone = document.querySelector('.driverPhone')
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
                stationTd1.textContent = `정류장${stationIndex + 1}`
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
const getRouteStatusData = (connectId) => {
    // 기존에 있던 데이터 다 삭제
    // console.log("BACk")
    // popupRouteStatusTbody.replaceWith(backupTbody.cloneNode(true))
    

    const searchData = {
        'id' : connectId,
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





// 기사 팝업

// "기상"
// "아침 점호 및 일일 점검"
// "노선명"
// "저녁 점호"
// "내일 배차 확인"
// "퇴근"

const searchDate = document.querySelector(".searchDate")
const driverPopupRoute = document.querySelector('.driverPopupRoute')
const driverPopupName = document.querySelector('.driverPopupName')
const driverPopupPhone = document.querySelector('.driverPopupPhone')
const driverPopupBus = document.querySelector('.driverPopupBus')
const popupDriverTbody = document.querySelector('#task-list')


function openDriverStatusPopup() {
    popupAreaModules[1].style.display = "block";
    const driverId = this.id
    getDriverStatusData(searchDate.value, driverId)
}

const createDailyDatas = (datas) => {
    console.log("datas", datas)
    popupDriverTbody.innerHTML = ""
    
    // 현재 노선정보
    driverPopupRoute.textContent = datas.info.route
    driverPopupName.textContent = datas.info.name
    driverPopupPhone.textContent = datas.info.phone
    driverPopupBus.textContent = datas.info.bus_num

    // 노선 정보 없을시 리턴
    if (!datas.tasks) return
    

    // 기상
    const wakeTime = `${addMinutes(datas.go_to_work.departure_time, -90)} ~ ${addMinutes(datas.go_to_work.departure_time, -60)}`
    const wakeTimeTr = document.createElement('tr');
    let wake_status = ""
    if (datas.go_to_work.has_issue) wake_status = "문제 발생"
    else if (datas.go_to_work.wake_time) wake_status = "완료"

    appendTd(wakeTimeTr, wakeTime, "기상", wake_status, datas.go_to_work.wake_time)
    popupDriverTbody.appendChild(wakeTimeTr)

    // 아침 점호 및 일일 점검
    const dailyChecklistTr = document.createElement("tr")
    appendTd(dailyChecklistTr, "-", "아침 점호 및 일일 점검", datas.go_to_work.daily_checklist.status, datas.go_to_work.daily_checklist.submit_time)
    popupDriverTbody.appendChild(dailyChecklistTr)

    // 노선
    datas.tasks.forEach(data => {
        const departureTime = addMinutes(data.departure_date, -90)
        const arrivalTime = addMinutes(data.arrival_date, 15)

        const tr = document.createElement("tr")
        const has_issue = data.has_issue
        appendTd(tr, `${departureTime} ~ ${arrivalTime}`, data.route, has_issue ? "문제 발생" : data.status, data.status_info[4].completion_time)
        popupDriverTbody.appendChild(tr)
    })
    
    // 퇴근 부분
    const getOffWorkData = datas.get_off_work
    const eveningChecklistTr = document.createElement("tr")
    appendTd(eveningChecklistTr, "-", "저녁 점호", getOffWorkData.roll_call_time ? "완료" : "", getOffWorkData.roll_call_time)
    popupDriverTbody.appendChild(eveningChecklistTr)

    const dispatchCheckTr = document.createElement("tr")
    appendTd(dispatchCheckTr, "-", "내일 배차 확인", getOffWorkData.tomorrow_dispatch_check_time ? "완료" : "", getOffWorkData.tomorrow_dispatch_check_time)
    popupDriverTbody.appendChild(dispatchCheckTr)

    const getOffWorkTr = document.createElement("tr")
    appendTd(getOffWorkTr, "-", "퇴근", getOffWorkData.get_off_time ? "완료" : "", getOffWorkData.get_off_time)
    popupDriverTbody.appendChild(getOffWorkTr)

    function appendTd(tr, text0, text1, text2, text3) {
        const td0 = document.createElement('td');
        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');

        td0.textContent = text0
        td1.textContent = text1
        td2.textContent = text2
        td3.textContent = text3

        tr.appendChild(td0)
        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)
    }

    // 문제 발생 클래스 적용
    Array.from(popupDriverTbody.children).forEach(tr => {
        if (tr.children[2].textContent == "문제 발생") {
            tr.children[2].setAttribute("class", "notDone")
        } else {
            tr.children[2].setAttribute("class", "")
        }
    })
}

// 정류장 목록 불러오기
const getDriverStatusData = (date, id) => {
    const searchData = {
        'date': date,
        'id': id
    }
    $.ajax({
        url: DRIVER_STATUS_URL,
        datatype: 'json',
        data: searchData,
        success: function (data) {
            // console.log(data);
            if (data.result == true) {
                createDailyDatas(data.data)
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
