const excelPopup = document.querySelector("#excelPopup")
const popupCloseBtn = document.querySelector(".popupCloseBtn")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")
const uploadCreateBtn = document.querySelector(".uploadCreateBtn")
const visibleLoading = document.querySelector(".visibleLoading")
const downloadExcelBtn = document.querySelector("#downloadExcelBtn")
const uploadExcelBtn = document.querySelector("#uploadExcelBtn")


let excelData = ""


uploadExcelBtn.addEventListener('click', () => {
    excelPopup.style.display = "block"
})

downloadExcelBtn.addEventListener('click', downloadExcel);

function downloadExcel() {
    if (confirm('정류장 목록을 다운로드 하시겠습니까?')) {
        window.location.href = DOWNLOAD_URL;
    }
}

excelUploadFile.addEventListener('change', readExcel)

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

uploadCreateBtn.addEventListener("click", dataParsing)

let uploadState = true

const dataParsingError = (error) => {
    excelUploadFile.value = ""
    excelUploadFileText.value = ""
    uploadState = true;
    alert(error)
}


function dataParsing(e) {
    e.preventDefault()

    if (uploadState) {

        uploadState = false;
        // 유효성검사
        //console.log("TEST", excelData);

        for (i = 0; i < excelData.length; i++) {
            if (excelData[i]["정류장명"] == undefined ||
                excelData[i]["주소"] == undefined ||
                excelData[i]["위도"] == undefined ||
                excelData[i]["경도"] == undefined) {
                dataParsingError(`${i + 1}번째 데이터의 필수 입력 사항이 입력되지 않았습니다.`)
                return;
            }

            let id = excelData[i]['id'];
            if ((id && !(Number.isInteger(parseInt(id))))) {
                dataParsingError(`${i + 1}번째 데이터의 id 항목이 형식에 맞지 않습니다.`)
                return;
            }
            if (excelData[i]['종류']) {
                const station_type = excelData[i]['종류'].split(", ")
                for (let j = 0; j < station_type.length; j++) {
                    const type = station_type[j];
                    if (type !== '차고지' &&
                        type !== '첫 정류장 대기장소' &&
                        type !== '정류장' &&
                        type !== '사업장' &&
                        type !== '대기장소' &&
                        type !== '마지막 정류장') {
                        dataParsingError(`${i + 1}번째 데이터의 종류 항목이 형식에 맞지 않습니다.`);
                        return;
                    }
                }
            }
        };

        visibleLoading.style.display = "block"

        let formatingData = []
        for (i = 0; i < excelData.length; i++) {
            let formatingObj = {
                id: excelData[i]["id"] == undefined ? "" : excelData[i]["id"],
                name: excelData[i]["정류장명"] == undefined ? "" : excelData[i]["정류장명"],
                address: excelData[i]["주소"] == undefined ? "" : excelData[i]["주소"],
                latitude: excelData[i]["위도"] == undefined ? "" : excelData[i]["위도"],
                longitude: excelData[i]["경도"] == undefined ? "" : excelData[i]["경도"],
                references: excelData[i]["참조사항"] == undefined ? "" : excelData[i]["참조사항"],
                station_type: excelData[i]["종류"] == undefined ? "" : excelData[i]["종류"],
            }
            formatingData.push(formatingObj)
        };
        console.log("DATAA", formatingData);
        $.ajax({
            url: UPLOAD_URL,
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
                } else if (data['error'] == 'driver_name') {
                    alert(`${data['count']}번째 데이터의 담당기사 이름이 맞지 않습니다.`)
                } else if (data['error'] == 'vehicle_id') {
                    alert(`${data['count']}번째 데이터의 차량id 항목이 맞지 않습니다.`)
                } else if (data['error'] == 'driver_id') {
                    alert(`${data['count']}번째 데이터의 담당기사id 항목이 맞지 않습니다.`)
                } else if (data['error'] == 'vehicle_num') {
                    alert(`${data['count']}번째 데이터의 차량번호 항목이 입력되지 않았습니다.`)
                } else if (data['error'] == 'driver_overlap') {
                    alert(`${data['count']}번째 데이터의 담당기사에게 이미 배정된 차량이 있습니다.`)
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