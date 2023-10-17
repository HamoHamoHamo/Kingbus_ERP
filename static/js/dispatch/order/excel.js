const excelUpload = document.querySelector(".excelUpload")
const excelPopup = document.querySelector("#excelPopup")
const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")
const uploadCrateBtn = document.querySelector(".uploadCrateBtn")
const visibleLoading = document.querySelector(".visibleLoading")
const downloadExcelBtn = document.querySelector("#downloadExcel")
const uploadExcelBtn = document.querySelector("#uploadExcel")
const excelDownloadForm = document.querySelector("#excelDownloadForm")
const excelDownloadDateInput = document.querySelectorAll(".excelDownloadDateInput")

let excelData = ""

excelDownloadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (confirm(`${excelDownloadDateInput[0].value}~${excelDownloadDateInput[1].value}\n일반 노선 목록을 다운로드 하시겠습니까?`))
    excelDownloadForm.submit();
})

uploadExcelBtn.addEventListener("click", () => {
    popupAreaModules[3].style.display = "block";
})

downloadExcelBtn.addEventListener('click',() => {
    popupAreaModules[4].style.display = "block";
    excelDownloadDateInput[0].value = searchDate[0].value;
    excelDownloadDateInput[1].value = searchDate[1].value;
})

popupBgModules[3].addEventListener("click", closeExcelPopup)
popupBgModules[4].addEventListener("click", closeExcelPopup)
SidemenuUseClose.addEventListener("click", closeExcelPopup)
popupCloseBtn[0].addEventListener("click", closeExcelPopup)
popupCloseBtn[1].addEventListener("click", closeExcelPopup)

function closeExcelPopup() {
    popupAreaModules[3].style.display = "none"
    popupAreaModules[4].style.display = "none"
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


		const regex = /^(?:20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]) (0\d|1\d|2[0-3]):([0-5]\d)$/;
        let column;

        for (i = 0; i < excelData.length; i++) {
            let errorLog = '';
            if (excelData[i]["출발지"] == undefined ||
                excelData[i]["도착지"] == undefined ||
                excelData[i]["출발날짜"] == undefined ||
                excelData[i]["복귀날짜"] == undefined ||
                excelData[i]["차량대수"] == undefined ||
                excelData[i]["예약자"] == undefined ||
                excelData[i]["예약자 전화번호"] == undefined ||
                excelData[i]["운행종류"] == undefined ||
                excelData[i]["계약금액"] == undefined ||
                excelData[i]["상여금"] == undefined)
            {
                errorLog = '데이터의 필수 입력 사항이 입력되지 않았습니다.';
            }
            // 날짜형식 확인
            else if (!(regex.test(excelData[i]['출발날짜'])) || !(regex.test(excelData[i]['복귀날짜'])))
                errorLog = '데이터의 출발날짜 또는 복귀날짜 항목이 형식에 맞지 않습니다.';
            else if (excelData[i]['출발날짜'] > excelData[i]['복귀날짜'])                
                errorLog = '데이터의 복귀날짜가 출발날짜보다 빠릅니다.';
            else if (excelData[i]["VAT포함여부"] !== 'y' && excelData[i]["VAT포함여부"] !== 'n')    
                errorLog = '데이터의 VAT포함여부 항목이 형식에 맞지 않습니다.';
            else if (excelData[i]["수금구분"] && excelData[i]["수금구분"] !== '회사수금' && excelData[i]["수금구분"] !== '현지수금' && excelData[i]["수금구분"] !== '계좌이체')
                errorLog = '데이터의 수금구분 항목이 형식에 맞지 않습니다.';
            else if (excelData[i]["결제방법"] && excelData[i]["결제방법"] !== '카드' && excelData[i]["결제방버법"] !== '현금')
                errorLog = '데이터의 결제방법 항목이 형식에 맞지 않습니다.';
            else if (isNaN(excelData[i]["계약금액"]))
                errorLog = '데이터의 계약금액 항목이 형식에 맞지 않습니다.';
            else if (isNaN(excelData[i]["상여금"]))
                errorLog = '데이터의 상여금 항목이 형식에 맞지 않습니다.';
            else if (isNaN(excelData[i]["차량대수"]))
                errorLog = '데이터의 차량대수 항목이 형식에 맞지 않습니다.';
            
            if (errorLog)
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 ${errorLog}`)
            }
        };

        visibleLoading.style.display = "block"

        let formatingData = []
        for (i = 0; i < excelData.length; i++) {
            let formatingObj = {
                id: excelData[i]["id"] == undefined ? "" : excelData[i]["id"],
                departure: excelData[i]["출발지"] == undefined ? "" : excelData[i]["출발지"],
                arrival: excelData[i]["도착지"] == undefined ? "" : excelData[i]["도착지"],
                departure_date: excelData[i]["출발날짜"] == undefined ? "" : excelData[i]["출발날짜"],
                arrival_date: excelData[i]["복귀날짜"] == undefined ? "" : excelData[i]["복귀날짜"],
                bus_cnt: excelData[i]["차량대수"] == undefined ? "" : excelData[i]["차량대수"].toString(),
                bus_type: excelData[i]["차량종류"] == undefined ? "" : excelData[i]["차량종류"],
                customer: excelData[i]["예약자"] == undefined ? "" : excelData[i]["예약자"],
                customer_phone: excelData[i]["예약자 전화번호"] == undefined ? "" : excelData[i]["예약자 전화번호"],
                contract_status: excelData[i]["계약현황"] == undefined ? "" : excelData[i]["계약현황"],
                operation_type: excelData[i]["운행종류"] == undefined ? "" : excelData[i]["운행종류"],
                reservation_company: excelData[i]["예약회사"] == undefined ? "" : excelData[i]["예약회사"],
                operating_company: excelData[i]["운행회사"] == undefined ? "" : excelData[i]["운행회사"],
                price: excelData[i]["계약금액"] == undefined ? "" : excelData[i]["계약금액"].toString(),
                driver_allowance: excelData[i]["상여금"] == undefined ? "" : excelData[i]["상여금"].toString(),
                option: excelData[i]["버스옵션"] == undefined ? "" : excelData[i]["버스옵션"],
                cost_type: excelData[i]["비용구분"] == undefined ? "" : excelData[i]["비용구분"],
                bill_place: excelData[i]["계산서 발행처"] == undefined ? "" : excelData[i]["계산서 발행처"],
                collection_type: excelData[i]["수금구분"] == undefined ? "" : excelData[i]["수금구분"],
                payment_method: excelData[i]["결제방법"] == undefined ? "" : excelData[i]["결제방법"],
                VAT: excelData[i]["VAT포함여부"] == undefined ? "" : excelData[i]["VAT포함여부"],
                ticketing_info: excelData[i]["표찰정보"] == undefined ? "" : excelData[i]["표찰정보"],
                order_type: excelData[i]["유형"] == undefined ? "" : excelData[i]["유형"],
                references: excelData[i]["참조사항"] == undefined ? "" : excelData[i]["참조사항"],
                driver_lease: excelData[i]["인력임대차"] == undefined ? "" : excelData[i]["인력임대차"],
                vehicle_lease: excelData[i]["차량임대차"] == undefined ? "" : excelData[i]["차량임대차"],
                waypoints: excelData[i]["경유지 정보"] == undefined ? "" : excelData[i]["경유지 정보"],
            }
            formatingData.push(formatingObj)
        };
        console.log("DATAA", formatingData);
        $.ajax({
            url: "/dispatch/order/route/upload",
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
                } else if (data['error'] == 'required') {
                    alert(`${data['line']}번째 데이터의 필수 입력 사항이 입력되지 않았습니다.`)
                } else if (data['error'] == 'id') {
                    alert(`${data['line']}번째 데이터의 id가 올바르지 않습니다.`)
                } else if (data['error'] == 'waypoints') {
                    alert(`${data['line']}번째 데이터의 경유지 항목이 형식에 맞지 않습니다.`)
                } else if (data['error'] == 'digit') {
                    alert(`${data['line']}번째 데이터의 차량대수 또는 계약금액 또는 상여금 항목이 형식에 맞지 않습니다.`)
                } else if (data['error'] == 'category') {
                    alert(`${data['line']}번째 데이터의 ${data['data']} 항목이 형식에 맞지 않습니다.`)
                } else {
                    alert('에러 발생\n' + data['error']);
                }
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return
            },
            error: function (request, status, error) {
                alert("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            },
        });
    }
}