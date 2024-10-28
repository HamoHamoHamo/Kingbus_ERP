const excelUpload = document.querySelector(".excelUpload")
const excelPopup = document.querySelector("#excelPopup")
const popupCloseBtn = document.querySelector(".popupCloseBtn")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")
const uploadCrateBtn = document.querySelector(".uploadCrateBtn")
const visibleLoading = document.querySelector(".visibleLoading")
const downloadExcelBtn = document.querySelector("#downloadExcel")

let excelData = ""

downloadExcelBtn.addEventListener('click', downloadExcel);

function downloadExcel() {
    if (confirm('차량 목록을 다운로드 하시겠습니까?')) {
        window.location.href=EXCEL_DOWNLOAD_URL;
    }
}

function readExcel() {

    excelUploadFileText.value = excelUploadFile.files[0].name

    let input = event.target;
    let reader = new FileReader();
    reader.onload = function () {
        let data = reader.result;
        let workBook = XLSX.read(data, { type: 'binary' });
        workBook.SheetNames.forEach(function (sheetName) {
            let rows = XLSX.utils.sheet_to_json(workBook.Sheets[sheetName]);
            excelData = JSON.stringify(rows);
            excelData = JSON.parse(excelData);
			console.log("excelData = ", excelData);
        })
    };
    reader.readAsBinaryString(input.files[0]);
}

uploadCrateBtn.addEventListener("click", dataParsing)

let uploadState = true

function dataParsing(e) {
    e.preventDefault()

    if (uploadState) {

        uploadState = false;
        // 유효성검사
        //console.log("TEST", excelData);

        
		const regex = RegExp(/^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$/);

        let column;

        for (i = 0; i < excelData.length; i++) {
            if (excelData[i]["차량번호 앞자리"] == undefined ||
                excelData[i]["차량번호"] == undefined)
            {
				excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 필수 입력 사항이 입력되지 않았습니다.`)
            }
            
            // 날짜형식 확인
            if (excelData[i]['출고일자'] && !(regex.test(excelData[i]['출고일자'])) || 
            (excelData[i]['정기점검일'] && !(regex.test(excelData[i]['정기점검일']))) ||
            (excelData[i]['보험납부일'] && !(regex.test(excelData[i]['보험납부일'])))) 
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                console.log('test', excelData[i]['출고일자'], excelData[i]['정기점검일'], excelData[i]['보험납부일'])
                return alert(`${i + 1}번째 데이터의 출고일자 또는 정기점검일 또는 보험납부일 항목이 형식에 맞지 않습니다.`)
            }
            if (excelData[i]["사용여부"] !== '사용' && excelData[i]["사용여부"] !== '미사용')
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 사용 항목이 형식에 맞지 않습니다.`)
            }
            let id = excelData[i]['id'];
            let driver_id = excelData[i]['담당기사id'];
            let garage_id = excelData[i]['차고지id'];
            if ((id && !(Number.isInteger(parseInt(id)))) || 
            driver_id && !(Number.isInteger(parseInt(driver_id))) ||
            garage_id && !(Number.isInteger(parseInt(garage_id))))
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 id 항목이 형식에 맞지 않습니다.`)
            }

            if (excelData[i]['연식'] && !(Number.isInteger(parseInt(excelData[i]['연식']))) ||
            excelData[i]['승차인원'] && !(Number.isInteger(parseInt(excelData[i]['승차인원']))) ||
            excelData[i]['차량가격'] && !(Number.isInteger(parseInt(excelData[i]['차량가격']))) ||
            excelData[i]['감가상각(월)'] && !(Number.isInteger(parseInt(excelData[i]['감가상각(월)']))) ||
            excelData[i]['번호판가격'] && !(Number.isInteger(parseInt(excelData[i]['번호판가격']))) ||
            excelData[i]['감가상각 기준 연도'] && !(Number.isInteger(parseInt(excelData[i]['감가상각 기준 연도']))) ||
            excelData[i]['보험비'] && !(Number.isInteger(parseInt(excelData[i]['보험비']))) ||
            excelData[i]['할부금액(월))'] && !(Number.isInteger(parseInt(excelData[i]['할부금액(월))']))) ||
            excelData[i]['남은 할부액'] && !(Number.isInteger(parseInt(excelData[i]['남은 할부액']))))
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터가 숫자 형식에 맞지 않습니다.`)
            }


            if ((excelData[i]['전광판유무'] && excelData[i]['전광판유무'] != true && excelData[i]['전광판유무'] != false) ||
            (excelData[i]['냉장고유무'] && excelData[i]['냉장고유무'] != true && excelData[i]['냉장고유무'] != false) ||
            (excelData[i]['노래방유무'] && excelData[i]['노래방유무'] != true && excelData[i]['노래방유무'] != false) ||
            (excelData[i]['USB유무'] && excelData[i]['USB유무'] != true && excelData[i]['USB유무'] != false) ||
            (excelData[i]['온수기유무'] && excelData[i]['온수기유무'] != true && excelData[i]['온수기유무'] != false) ||
            (excelData[i]['tv유무'] && excelData[i]['tv유무'] != true && excelData[i]['tv유무'] != false))
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터가 TRUE 또는 FALSE 형식에 맞지 않습니다.`)
            }
        };

        visibleLoading.style.display = "block"

        let formatingData = []
        for (i = 0; i < excelData.length; i++) {
            let formatingObj = {
                id: excelData[i]["id"] == undefined ? "" : excelData[i]["id"],
                vehicle_num0: excelData[i]["차량번호 앞자리"] == undefined ? "" : excelData[i]["차량번호 앞자리"],
                vehicle_num: excelData[i]["차량번호"] == undefined ? "" : excelData[i]["차량번호"],
                vehicle_id: excelData[i]["차대번호"] == undefined ? "" : excelData[i]["차대번호"],
                motor_type: excelData[i]["원동기형식"] == undefined ? "" : excelData[i]["원동기형식"],
                rated_output: excelData[i]["정격출력"] == undefined ? "" : excelData[i]["정격출력"],
                vehicle_type: excelData[i]["차량이름"] == undefined ? "" : excelData[i]["차량이름"],
                maker: excelData[i]["제조사"] == undefined ? "" : excelData[i]["제조사"],
                model_year: excelData[i]["연식"] == undefined ? "" : excelData[i]["연식"],
                release_date: excelData[i]["출고일자"] == undefined ? "" : excelData[i]["출고일자"],
                driver: excelData[i]["담당기사id"] == undefined ? "" : excelData[i]["담당기사id"],
                use: excelData[i]["사용여부"] == undefined ? "" : excelData[i]["사용여부"],
                passenger_num: excelData[i]["승차인원"] == undefined ? "" : excelData[i]["승차인원"],
                check_date: excelData[i]["정기점검일"] == undefined ? "" : excelData[i]["정기점검일"],
                type: excelData[i]["형식"] == undefined ? "" : excelData[i]["형식"],
                garage: excelData[i]["차고지id"] == undefined ? "" : excelData[i]["차고지id"],
                remark: excelData[i]["비고"] == undefined ? "" : excelData[i]["비고"],
                vehicle_price: excelData[i]["차량가격"] == undefined ? "" : excelData[i]["차량가격"],
                depreciation_month: excelData[i]["감가상각(월)"] == undefined ? "" : excelData[i]["감가상각(월)"],
                number_price: excelData[i]["번호판가격"] == undefined ? "" : excelData[i]["번호판가격"],
                depreciation_year: excelData[i]["감가상각 기준 연도"] == undefined ? "" : excelData[i]["감가상각 기준 연도"],
                insurance_pay_date: excelData[i]["보험납부일"] == undefined ? "" : excelData[i]["보험납부일"],
                insurance_price: excelData[i]["보험비"] == undefined ? "" : excelData[i]["보험비"],
                monthly_installment: excelData[i]["할부금액(월)"] == undefined ? "" : excelData[i]["할부금액(월)"],
                remaining_installment_amount: excelData[i]["남은 할부액"] == undefined ? "" : excelData[i]["남은 할부액"],
                led: excelData[i]["전광판유무"] == undefined ? "" : excelData[i]["전광판유무"],
                fridge: excelData[i]["냉장고유무"] == undefined ? "" : excelData[i]["냉장고유무"],
                sing: excelData[i]["노래방유무"] == undefined ? "" : excelData[i]["노래방유무"],
                usb: excelData[i]["USB유무"] == undefined ? "" : excelData[i]["USB유무"],
                water_heater: excelData[i]["온수기유무"] == undefined ? "" : excelData[i]["온수기유무"],
                tv: excelData[i]["tv유무"] == undefined ? "" : excelData[i]["tv유무"],
            }
            formatingData.push(formatingObj)
        };
        console.log("DATAA", formatingData);
        $.ajax({
            url: "/vehicle/list/upload",
            method: "POST",
            data: JSON.stringify(formatingData),
            datatype: 'json',
            success: function (data) {
                visibleLoading.style.display = "none"
                uploadState = true
                console.log("success data", data);
                if (data['status'] == 'success') {
                    alert(`${data['count']}개의 데이터가 저장되었습니다`);
                    location.reload();
                } else if (data['error'] == 'vehicle_id') {
                    alert(`${data['count']}번째 데이터의 차량id 항목이 맞지 않습니다.`) 
                } else if (data['error'] == 'driver_id') {
                    alert(`${data['count']}번째 데이터의 담당기사id 항목이 맞지 않습니다.`) 
                } else if (data['error'] == 'vehicle_num') {
                    alert(`${data['count']}번째 데이터의 차량번호 항목이 입력되지 않았습니다.`) 
                } else if (data['error'] == 'driver_overlap') {
                    alert(`${data['count']}번째 데이터의 담당기사에게 이미 배정된 차량이 있습니다.`) 
                } else if (data['error'] == 'garage_id') {
                    alert(`${data['count']}번째 데이터의 차고지id 항목이 맞지 않습니다.`) 
                } else {
                    alert('에러 발생\n' + data['error']);
                }
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return
            },
            error: function (request, status, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            },
        });
    }
}