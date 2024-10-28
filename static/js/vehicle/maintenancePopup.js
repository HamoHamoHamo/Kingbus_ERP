const openMaintenancePopupBtn = document.querySelectorAll(".openMaintenancePopupBtn")
const maintenanceForm = document.querySelector(".maintenanceForm")
const maintenanceVehicleHidden = document.querySelectorAll(".maintenanceVehicleHidden")
const total_maintenance_cost = document.querySelector(".total_maintenance_cost")
const total_tuning_cost = document.querySelector(".total_tuning_cost")
const popupMaintenanceTbody = document.querySelector(".popupMaintenanceTbody")
const maintenancePopupDate1 = document.querySelector('#maintenancePopupDate1')
const maintenancePopupDate2 = document.querySelector('#maintenancePopupDate2')
const maintenancePopupType = document.querySelector('#maintenancePopupType')

const maintenanceDeleteForm = document.querySelector(".maintenanceDeleteForm")
const maintenanceDeleteBtn = document.querySelector("#maintenanceDeleteBtn")
const maintenancePopupSearchBtn = document.querySelector("#maintenancePopupSearchBtn")

maintenanceDeleteBtn.addEventListener("click", () => {
    if (confirm("정말로 삭제하시겠습니까?")) {
        maintenanceDeleteForm.submit()
    }
})

let maintenancePopupVehicleId = ''
Array.from(openMaintenancePopupBtn).forEach(item => item.addEventListener("click", openMaintenancePopup))


maintenancePopupSearchBtn.addEventListener("click", () => getMaintenanceListData(maintenancePopupVehicleId))

function openMaintenancePopup() {
    popupAreaModules[2].style.display = "block"
    const index = this.parentNode.classList[1]
    maintenancePopupVehicleId = this.parentNode.classList[0]

    Array.from(maintenanceVehicleHidden).forEach(item => item.value=maintenancePopupVehicleId)
    
    total_maintenance_cost.innerText = `${parseInt(vehicleDatas[index].total_maintenance_cost).toLocaleString()} 원`
    total_tuning_cost.innerText = `${parseInt(vehicleDatas[index].total_tuning_cost).toLocaleString()} 원`


    maintenancePopupDate1.value = ''
    maintenancePopupDate2.value = ''
    maintenancePopupType.value = ''
    getMaintenanceListData(maintenancePopupVehicleId)
}


const createDatas = (datas) => {
    
    const headers = [
        'type',
        'work_date',
        'content',
        'cost',
    ]
    console.log("datas", datas)

    datas?.forEach((data, index) => {
        const tr = document.createElement('tr');

        const checkboxTd = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.setAttribute("type", "checkbox")
        checkbox.setAttribute("value", data.id)
        checkbox.setAttribute("name", "id")
        checkboxTd.appendChild(checkbox)
        tr.appendChild(checkboxTd)

        const indexTd = document.createElement('td');
        indexTd.textContent = index + 1;
        tr.appendChild(indexTd);

        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = header == 'cost' ? data[header].toLocaleString() : data[header];
            tr.appendChild(td);
        });

        popupMaintenanceTbody.appendChild(tr)
    })
}

// 정류장 목록 불러오기
const getMaintenanceListData = (vehicleId) => {
    // 기존에 있던 데이터 다 삭제
    popupMaintenanceTbody.innerHTML = ''

    const searchData = {
        'date1' : maintenancePopupDate1.value,
        'date2' : maintenancePopupDate2.value,
        'search_type' : maintenancePopupType.value,
        'pk' : vehicleId,
    }
    $.ajax({
        url: MAINTENANCE_LIST_URL,
        datatype: 'json',
        data: searchData,
        success: function (data) {
            console.log(data);
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

