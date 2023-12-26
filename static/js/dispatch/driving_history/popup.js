const morningPopup = document.querySelectorAll(".morningPopup");
const eveningPopup = document.querySelectorAll(".eveningPopup");
const drivingPopup = document.querySelectorAll(".drivingPopup");
const popupAreaModules = document.querySelectorAll(".popupAreaModules");
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const popupCloseBtn = document.querySelectorAll(".closeBtn")
const morningPopupData = document.querySelectorAll(".morningPopupData")
const eveningPopupData = document.querySelectorAll(".eveningPopupData")
const date = document.querySelector(".searchDateInput")
const popupListBox = document.querySelector(".shcedulePopupTableBody tbody")

//팝업닫기
for (i = 0; i < popupAreaModules.length; i++) {
    popupBgModules[i].addEventListener("click", closePopup)
    popupCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    for (i = 0; i < popupAreaModules.length; i++) {
        popupAreaModules[i].style.display = "none"
    }
}
//아침점호팝업 열기
for (i = 0; i < morningPopup.length; i++) {
    morningPopup[i].addEventListener("click", openMorningDetailPopup)
}

function openMorningDetailPopup() {
    popupAreaModules[0].style.display = "block";
    morningPopupData[0].innerText = morningData[this.parentNode.className].arrival_time;
    morningPopupData[1].innerText = morningData[this.parentNode.className].vehicle_list;
    morningPopupData[2].innerText = morningData[this.parentNode.className].health_condition;
    morningPopupData[3].innerText = morningData[this.parentNode.className].cleanliness_condition;
    morningPopupData[4].innerText = morningData[this.parentNode.className].route_familiarity;
    morningPopupData[5].innerText = morningData[this.parentNode.className].alcohol_test;
}

//저녁점호팝업 열기
for (i = 0; i < eveningPopup.length; i++) {
    eveningPopup[i].addEventListener("click", openEveningDetailPopup)
}

function openEveningDetailPopup() {
    popupAreaModules[2].style.display = "block";
    eveningPopupData[0].innerText = eveningData[this.parentNode.className].vehicle;
    eveningPopupData[1].innerText = eveningData[this.parentNode.className].garage_location;
    eveningPopupData[2].innerText = eveningData[this.parentNode.className].battery_condition;
    eveningPopupData[3].innerText = eveningData[this.parentNode.className].drive_distance;
    eveningPopupData[4].innerText = eveningData[this.parentNode.className].fuel_quantity;
    eveningPopupData[5].innerText = eveningData[this.parentNode.className].urea_solution_quantity;
    eveningPopupData[6].innerText = eveningData[this.parentNode.className].suit_gauge;
    eveningPopupData[7].innerText = eveningData[this.parentNode.className].special_notes;
}


function getDrivingHistory(date, id, createElements) {
    const parameter = {
        date : date,
        member_id : id
    }
    response = $.ajax({
        url: driving_history_url,
        method: "GET",
        data: parameter,
        datatype: 'json',
        success: (response) => {
            if (response.result == 'true') {
                createElements(response);
                return
            } else { 
                //loadingBg.style.display = "none"
                alert("운행일보를 불러오지 못했습니다.")
                console.log(response)
            }
        },
        error: function (request, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}

function createDrivingHistoryElements(data) {
    console.log("RESPONSE", data);

    for (i = 0; i < data.driving_history_values.length; i++) {
        
        let curData = data.driving_history_values[i];
        let connectData = data.connect_data_list[i];
        
        const newTr = document.createElement('tr');
        const newTdType = document.createElement('td');
        const newTdBus = document.createElement('td');
        const newTdTime = document.createElement('td');
        const newTdRout = document.createElement('td');
        const newTdArrivalKm = document.createElement('td');
        const newTdDepartureKm = document.createElement('td');
        const newTdPassenger_num = document.createElement('td');
        const newTdSpecialNotes = document.createElement('td');

        
        const newTextType = document.createTextNode(connectData.work_type);
        const newTextTimeDepartureAll = document.createTextNode(`${connectData.departure_date}~`);
        const newTextTimeArrivalAll = document.createTextNode(`${connectData.arrival_date}`);
        const newTextTimeDeparture = document.createTextNode(`${connectData.departure_date.substr(11,)}~`);
        const newTextTimeArrival = document.createTextNode(`${connectData.arrival_date.substr(11,)}`);
        const newTextRouteDeparture = document.createTextNode(`${connectData.departure}▶`);
        const newTextRouteArrival = document.createTextNode(`${connectData.arrival}`);
        const newTextBus = document.createTextNode(connectData.bus);
        const newTextArrivalKm = document.createTextNode(curData.arrival_km);
        const newTextDepartureKm = document.createTextNode(curData.departure_km);
        const newTextPassenger_num = document.createTextNode(curData.passenger_num);
        const newTextSpecialNotes = document.createTextNode(curData.special_notes);

        newTdType.appendChild(newTextType);
        if (connectData.work_type == "일반") {
            newTdTime.appendChild(newTextTimeDepartureAll);
            newTdTime.appendChild(document.createElement('br'));
            newTdTime.appendChild(newTextTimeArrivalAll);
        } else {
            newTdTime.appendChild(newTextTimeDeparture);
            newTdTime.appendChild(newTextTimeArrival);
        }
        newTdRout.appendChild(newTextRouteDeparture);
        newTdRout.appendChild(document.createElement('br'));
        newTdRout.appendChild(newTextRouteArrival);
        newTdBus.appendChild(newTextBus);
        newTdArrivalKm.appendChild(newTextArrivalKm);
        newTdDepartureKm.appendChild(newTextDepartureKm);
        newTdPassenger_num.appendChild(newTextPassenger_num);
        newTdSpecialNotes.appendChild(newTextSpecialNotes);

        newTr.appendChild(newTdType);
        newTr.appendChild(newTdBus);
        newTr.appendChild(newTdTime);
        newTr.appendChild(newTdRout);
        newTr.appendChild(newTdArrivalKm);
        newTr.appendChild(newTdDepartureKm);
        newTr.appendChild(newTdPassenger_num);
        newTr.appendChild(newTdSpecialNotes);
        popupListBox.appendChild(newTr);
    }
}

//운행일보팝업 열기
for (i = 0; i < drivingPopup.length; i++) {
    drivingPopup[i].addEventListener("click", openDrivingDetailPopup)
}

function removeChild(element) {

    console.log("COUNT", element.childElementCount, element.children);
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function openDrivingDetailPopup() {
    popupAreaModules[1].style.display = "block";
    
    removeChild(popupListBox);

    const data = getDrivingHistory(date.value, this.id, data => {
        createDrivingHistoryElements(data)
    });

    if (!data) {
        return
    }
    //console.log("TEST", data);
    //console.log("TEST", data.responseJSON);
}