const openPhotoPopupBtn = document.querySelectorAll('.openPhotoPopupBtn')
const photoVehicleHidden = document.querySelectorAll(".photoVehicleHidden")

const photoPopupDate1 = document.querySelector('#photoPopupDate1')
const photoPopupDate2 = document.querySelector('#photoPopupDate2')
const photoPopupType = document.querySelector('#photoPopupType')
const popupPhotoTbody = document.querySelector(".popupPhotoTbody")
const photoPopupSearchBtn = document.querySelector("#photoPopupSearchBtn")


const photoDeleteForm = document.querySelector(".photoDeleteForm")
const photoDeleteBtn = document.querySelector("#photoDeleteBtn")

photoDeleteBtn.addEventListener("click", () => {
    if (confirm("정말로 삭제하시겠습니까?")) {
        photoDeleteForm.submit()
    }
})

let photoPopupVehicleId = ''
photoPopupSearchBtn.addEventListener("click", () => getPhotoListData(photoPopupVehicleId))

Array.from(openPhotoPopupBtn).forEach(item => item.addEventListener("click", openPhotoPopup))


function openPhotoPopup() {
    popupAreaModules[4].style.display = "block"

    photoPopupVehicleId = this.parentNode.classList[0]
    Array.from(photoVehicleHidden).forEach(item => item.value=photoPopupVehicleId)

    photoPopupDate1.value = ''
    photoPopupDate2.value = ''
    photoPopupType.value = ''
    getPhotoListData(photoPopupVehicleId)
}


const createPhotoListDatas = (datas) => {
    
    const headers = [
        'type',
        'date',
        'driver_id__name',
        'filename',
    ]
    console.log("datas", datas)

    datas?.forEach((data, index) => {
        if (data == 'path') return
        console.log("TEST", data)
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
            td.textContent = data[header];
            if (header == 'filename') {
                td.setAttribute("class", "bluelink")
                td.addEventListener("click", () => window.open(`photo/image/${data['id']}`, "image", "width=630, height=891"))
            }
            tr.appendChild(td);
        });

        popupPhotoTbody.appendChild(tr)
    })
}


// 정류장 목록 불러오기
const getPhotoListData = (vehicleId) => {
    // 기존에 있던 데이터 다 삭제
    popupPhotoTbody.innerHTML = ''

    const searchData = {
        'date1' : photoPopupDate1.value,
        'date2' : photoPopupDate2.value,
        'search_type' : photoPopupType.value,
        'pk' : vehicleId,
    }
    $.ajax({
        url: PHOTO_LIST_URL,
        datatype: 'json',
        data: searchData,
        success: function (data) {
            console.log(data);
            if (data.result == true) {
                createPhotoListDatas(data.data)
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

