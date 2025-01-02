import { addEventClosePopup, closePopup } from "/static/js/common/popupCommon.js"
addEventClosePopup()

const popupAreaModules = document.querySelectorAll('.popupAreaModules')
const addPopupOpenBtn = document.querySelector('.addPopupOpenBtn')
const assignmentForm = document.querySelector('.assignmentForm')
const popupTitle = document.querySelector('.popupTitle')
const sendToHidden = document.querySelector('.sendToHidden')
const submitBtn = document.querySelector('.submitBtn')
const deleteBtn = document.querySelector('.deleteBtn')
const tableBodyTrList = document.querySelectorAll('.tableBody .tr')
const noPopup = document.querySelectorAll('.noPopup')

document.querySelector('.closeBtn').addEventListener('click', closePopup)

function clearTableBody() {
    const tbody = popupDataTable.querySelector('tbody');
    if (tbody) {
        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }
    }
}

// 수정 팝업
Array.from(tableBodyTrList).forEach(item => {
    item.addEventListener('click', openEditPopup)
})
function openEditPopup() {
    popupAreaModules[0].style.display = "block"

    // thead 빼고 다 지우기
    clearTableBody()

    // 업무수정 팝업으로 변경
    popupTitle.textContent = "공차 데이터"
    const id = this.classList[1]
    sendToHidden.value = id

    getDetailData(id)
}

// 상세 정보 받기
function getDetailData(id) {
    $.ajax({
        url: DETAIL_URL,
        method: "GET",
        data: {
            'id' : id,
        },
        datatype: 'json',
        success: function (data) {
            // visibleLoading.style.display = "none"
            console.log("API DATA", data)
            if (data['result'] == true) {
                console.log("success data", data);
                setDetailDatas(data.data);
            } else {
                console.log("ERROR", data);
                alert('에러 발생\n' + data.meta);
            }
            return
        },
        error: function (request, status, error) {
            alert("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}

// 상세 정보 팝업에 값 넣기
const popupDataTable = document.querySelector('.popupDataTable')
const popupDataTableBody = document.querySelector('.popupDataTableBody')
function setDetailDatas(datas) {

    datas?.forEach(emptyRun => {
        const tr = document.createElement('tr')
        const route = createTd(emptyRun.arrival_data_id__route)
        const departure_time = createTd(emptyRun.arrival_data_id__departure_time)
        const departure = createTd(emptyRun.arrival_data_id__departure)
        const arrival_time = createTd(emptyRun.arrival_data_id__arrival_time)
        const arrival = createTd(emptyRun.arrival_data_id__arrival)
        const week = createTd(emptyRun.arrival_data_id__week)
        const duration = createTd(emptyRun.duration)
        const distance = createTd(`${emptyRun.distance}m`)
        const can_drive = createTd(emptyRun.can_drive)
        const regularly_data_id__arrival_time = createTd(emptyRun.regularly_data_id__arrival_time)
        
        tr.appendChild(regularly_data_id__arrival_time)
        tr.appendChild(duration)
        tr.appendChild(createTd((`${emptyRun.arrival_data_id__departure_time} ~ ${emptyRun.arrival_data_id__arrival_time}`)))
        tr.appendChild(route)
        tr.appendChild(distance)
        tr.appendChild(departure)
        tr.appendChild(arrival)
        tr.appendChild(week)
        tr.appendChild(can_drive)
        if (emptyRun.can_drive == false) {
            tr.classList.add('cantDrive')
        }

        popupDataTableBody.appendChild(tr)
    })
}

function createTd(data) {
    const td = document.createElement('td')
    td.textContent = data
    return td
}