const scheduleDriver = document.querySelectorAll('.tdDriver')
const popupAreaModules = document.querySelector('.popupAreaModules')
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelector(".PopupBtnBox div")
const deiverName = document.querySelector(".deiverName")
const vehicleNum = document.querySelector(".vehicleNum")
const dispatchDate = document.querySelector(".dispatchDate")
const dispatchDateFilter = document.querySelector(".dateFilterBox input")
const popupListBox = document.querySelector(".shcedulePopupTableBody tbody")
const tr = document.querySelectorAll(".tr")


for (i = 0; i < scheduleDriver.length; i++) {
    scheduleDriver[i].addEventListener('click', openScheduleDetail)
}

const removeSpecial = /\(([^)]+)\)/;
function openScheduleDetail() {
    popupAreaModules.style.display = 'block'
    deiverName.innerText = removeSpecial.exec(this.childNodes[3].innerText)[1]
    vehicleNum.innerText = this.childNodes[1].innerText
    dispatchDate.innerText = dispatchDateFilter.value;

    for (i = 0; i < data[this.childNodes[1].className].length; i++) {
        const newTr = document.createElement('tr');
        const newTdType = document.createElement('td');
        const newTdTime = document.createElement('td');
        const newTdRout = document.createElement('td');
        const newTextType = document.createTextNode(`${data[this.childNodes[1].className][i].work_type}`);
        const newTextTimeDepartureAll = document.createTextNode(`${data[this.childNodes[1].className][i].departure_date.replace(/T/g, " ")}~`);
        const newTextTimeArrivalAll = document.createTextNode(`${data[this.childNodes[1].className][i].arrival_date.replace(/T/g, " ")}`);
        const newTextTimeDeparture = document.createTextNode(`${data[this.childNodes[1].className][i].departure_date.substr(11,)}~`);
        const newTextTimeArrival = document.createTextNode(`${data[this.childNodes[1].className][i].arrival_date.substr(11,)}`);
        const newTextRoutDeparture = document.createTextNode(`${data[this.childNodes[1].className][i].departure}▶`);
        const newTextRoutArrival = document.createTextNode(`${data[this.childNodes[1].className][i].arrival}`);
        newTdType.appendChild(newTextType);
        if (data[this.childNodes[1].className][i].work_type == "일반") {
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
        newTr.appendChild(newTdType);
        newTr.appendChild(newTdTime);
        newTr.appendChild(newTdRout);
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

window.onload = function () {
    for (i = 0; i < data.length; i++) {
        for (j = 0; j < data[i].length; j++) {
            if (data[i][j].work_type == "일반") {
                if (data[i][j].departure_date.substr(0, 10) == data[i][j].arrival_date.substr(0, 10)) {
                    startH = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(0, 2)
                    startM = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(2,)
                    endH = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(0, 2)
                    endM = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(2,)
                    const order = document.createElement('div');
                    order.setAttribute("class", "orderLine");
                    order.setAttribute("style", `left: ${((startH * 60 + startM) * 0.058) / 100}%; width: ${(((endH * 60 + endM) - (startH * 60 + startM)) * 0.058) / 100}%;`);
                    tr[i].appendChild(order);
                } else if (data[i][j].departure_date.substr(0, 10) == dispatchDateFilter.value) {
                    startH = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(0, 2)
                    startM = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(2,)
                    const order = document.createElement('div');
                    order.setAttribute("class", "orderLine");
                    order.setAttribute("style", `left: ${(((startH * 60 + startM) * 0.058) / 100) - 0.1}%; width: ${100 - (((startH * 60 + startM) * 0.058) / 100) - 16.38}%;`);
                    tr[i].appendChild(order);
                } else if (data[i][j].arrival_date.substr(0, 10) == dispatchDateFilter.value) {
                    endH = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(0, 2)
                    endM = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(2,)
                    const order = document.createElement('div');
                    order.setAttribute("class", "orderLine");
                    order.setAttribute("style", `left: 0%; width: ${(((endH * 60 + endM) * 0.058) / 100) - 0.1}%;`);
                    tr[i].appendChild(order);
                } else {
                    const order = document.createElement('div');
                    order.setAttribute("class", "orderLine");
                    order.setAttribute("style", `left: 0%; width: 83.52%;`);
                    tr[i].appendChild(order);
                }
            } else {
                startH = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(0, 2)
                startM = data[i][j].departure_date.substr(11,).replace(/:/g, "").substr(2,)
                endH = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(0, 2)
                endM = data[i][j].arrival_date.substr(11,).replace(/:/g, "").substr(2,)
                const regularly = document.createElement('div');
                regularly.setAttribute("class", "regularlyLine");
                regularly.setAttribute("style", `left: ${((startH * 60 + startM) * 0.058) / 100}%; width: ${(((endH * 60 + endM) - (startH * 60 + startM)) * 0.058) / 100}%;`);
                tr[i].appendChild(regularly);
            }
        }
    }
}