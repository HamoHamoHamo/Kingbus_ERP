const excelUpload = document.querySelector(".excelUpload")
const excelPopup = document.querySelector("#excelPopup")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")
const uploadCrateBtn = document.querySelector(".uploadCrateBtn")
const visibleLoading = document.querySelector(".visibleLoading")

let parms = new URLSearchParams(location.search)


excelUpload.addEventListener("click", openUploadPopup)

function openUploadPopup() {
    excelPopup.style.display = "block"
}

let excelData = ""

excelUploadFile.addEventListener("change", readExcel)

function readExcel() {
    excelUploadFileText.value = excelUploadFile.files[0].name

    let input = event.target;
    let reader = new FileReader();
    reader.onload = function () {
        let data = reader.result;
        let workBook = XLSX.read(data, { type: 'binary' });
        workBook.SheetNames.forEach(function (sheetName) {
            console.log('SheetName: ' + sheetName);
            let rows = XLSX.utils.sheet_to_json(workBook.Sheets[sheetName]);
            excelData = JSON.stringify(rows);
            excelData = JSON.parse(excelData)
        })
    };
    reader.readAsBinaryString(input.files[0]);
}

uploadCrateBtn.addEventListener("click", dateFormat)

let uploadState = true

function dateFormat(e) {
    e.preventDefault()

    if (uploadState) {

        uploadState = false;
        // 유효성검사
        //console.log("TEST", excelData);

        
        const regex = /^(0[0-9]|1[0-9]|2[0-3]):(0[1-9]|[0-5][0-9])$/;
        const regexMonth = RegExp(/^\d{4}-(0[1-9]|1[012])$/);
        const numberPattern = /^\d+$/;

        for (i = 0; i < excelData.length; i++) {
            if (excelData[i]["그룹"] == undefined ||
                excelData[i]["노선명"] == undefined ||
                excelData[i]["출발지"] == undefined ||
                excelData[i]["도착지"] == undefined ||
                excelData[i]["순번1"] == undefined ||
                excelData[i]["순번2"] == undefined ||
                excelData[i]["출발시간"] == undefined ||
                excelData[i]["도착시간"] == undefined ||
                excelData[i]["출/퇴근"] == undefined ||
                excelData[i]["운행요일"] == undefined ||
                excelData[i]["금액"] == undefined ||
                excelData[i]["기사수당(현재)"] == undefined ||
                excelData[i]["기사수당(변경)"] == undefined ||
                excelData[i]["용역수당"] == undefined ||
                excelData[i]["사용"] == undefined)
            {
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 필수 입력 사항이 입력되지 않았습니다.`)
            }
            console.log("기준일 테스트", excelData[i]['기준일']);
            // 기준일
            if (excelData[i]['기준일'] && !(regexMonth.test(excelData[i]['기준일']))) {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 기준일이 형식에 맞지 않습니다.`)
            }
            // 운행시간
            if (!(regex.test(excelData[i].출발시간)) || !(regex.test(excelData[i].도착시간))) {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 운행시간이 형식에 맞지 않습니다.`)
            }
            // 출/퇴근
            if (excelData[i]["출/퇴근"] !== "출근" && excelData[i]["출/퇴근"] !== "퇴근") {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 출/퇴근 항목이 형식에 맞지 않습니다.`)
            }
            // 운행요일
            let weekCheck = excelData[i].운행요일.split(" ");
            for (j = 0; j < weekCheck.length; j++) {
                if (weekCheck[j] !== "월" && weekCheck[j] !== "화" && weekCheck[j] !== "수" && weekCheck[j] !== "목" && weekCheck[j] !== "금" && weekCheck[j] !== "토" && weekCheck[j] !== "일") {
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    uploadState = true;
                    return alert(`${i + 1}번째 데이터의 운행요일 항목이 형식에 맞지 않습니다.`)
                }
            };
            console.log("TEST", excelData[i]["사용"])
            if (excelData[i]["사용"] !== '사용' && excelData[i]["사용"] !== '미사용')
            {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 사용 항목이 형식에 맞지 않습니다.`)
            }
            if (excelData[i]['거리'] && !(numberPattern.test(excelData[i]['거리']))) {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                uploadState = true;
                return alert(`${i + 1}번째 데이터의 거리 항목이 형식에 맞지 않습니다.`)
            }
        };


        visibleLoading.style.display = "block"

        let formatingData = []
        for (i = 0; i < excelData.length; i++) {
            let formatingObj = {
                id: excelData[i]["id"] == undefined ? "" : excelData[i]["id"],
                group: excelData[i]["그룹"],
                route: excelData[i]["노선명"],
                departure: excelData[i]["출발지"],
                arrival: excelData[i]["도착지"],
                number1: excelData[i]["순번1"],
                number2: excelData[i]["순번2"],
                departure_time: excelData[i]["출발시간"],
                arrival_time: excelData[i]["도착시간"],
                work_type: excelData[i]["출/퇴근"],
                location: excelData[i]["위치"] == undefined ? "" : excelData[i]["위치"],
                week: excelData[i]['운행요일'],
                distance: excelData[i]['거리'],
                detailed_route: excelData[i]["상세노선"] == undefined ? "" : excelData[i]["상세노선"],
                maplink: excelData[i]["카카오맵"] == undefined ? "" : excelData[i]["카카오맵"],
                waypoint: excelData[i]["경유지"] == undefined ? "" : excelData[i]["경유지"],
                price: excelData[i]["금액"],
                driver_allowance: excelData[i]["기사수당(현재)"],
                driver_allowance2: excelData[i]["기사수당(변경)"],
                outsourcing_allowance: excelData[i]["용역수당"],
                month: excelData[i]["기준일"] == undefined ? "" : excelData[i]["기준일"],
                references: excelData[i]["참조사항"] == undefined ? "" : excelData[i]["참조사항"],
                use: excelData[i]["사용"],
            }
            formatingData.push(formatingObj)
        };
        console.log("DATAA", formatingData);
        $.ajax({
            url: "/dispatch/regularly/route/upload",
            method: "POST",
            data: JSON.stringify(formatingData),
            datatype: 'json',
            success: function (data) {
                visibleLoading.style.display = "none"
                uploadState = true
                console.log("DATASS", data);
                if (data['error'] == 'group') {
                    alert(`${data['line']}번째 데이터의 그룹 항목 ${data['data']} 가 그룹목록에 존재하지 않습니다.`)
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    uploadState = true;
                    return;
                } else if (data['error'] == 'required') {
                    alert(`${data['line']}번째 데이터의 필수 입력 사항이 입력되지 않았습니다.`)
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    uploadState = true;
                    return;
                } else if (data['error'] == 'id') {
                    alert(`${data['line']}번째 데이터의 id가 올바르지 않습니다.`)
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    uploadState = true;
                    return;
                }
                else if (data['count']) {
                    alert(`${data['count']}개의 데이터가 저장되었습니다`);

                    location.reload();

                } else {
                    alert('에러 발생\n' + data['error']);
                }
            },
            error: function (request, status, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            },
        });
    }
}