const excelUpload = document.querySelector(".excelUpload")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const excelPopupCloseBtn = document.querySelector(".excelPopupCloseBtn")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")
const uploadCrateBtn = document.querySelector(".uploadCrateBtn")
const visibleLoading = document.querySelector(".visibleLoading")

let parms = new URLSearchParams(location.search)

excelUpload.addEventListener("click", openUploadPopup)

function openUploadPopup() {
    if(parms.has("id")){
        popupAreaModules[1].style.display = "block"
    }else{
        popupAreaModules[0].style.display = "block"
    }
}

if(parms.has("id")){
    popupBgModules[1].addEventListener("click", closePopup)
}else{
    popupBgModules[0].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)
excelPopupCloseBtn.addEventListener("click", closePopup)

function closePopup() {
    if(parms.has("id")){
        popupAreaModules[1].style.display = "none"
    }else{
        popupAreaModules[0].style.display = "none"
    }
    popupAreaModules[1].style.display = "none"
    excelUploadFile.value = ""
    excelUploadFileText.value = ""
}

let excelData = ""

function readExcel() {

    excelUploadFileText.value = excelUploadFile.files[0].name

    let input = event.target;
    let reader = new FileReader();
    reader.onload = function () {
        let data = reader.result;
        let workBook = XLSX.read(data, { type: 'binary', cellDates: true, dateNF: 'yyyy-mm-dd' });
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

        // 순번
        for (i = 0; i < excelData.length; i++) {
            if (!`${excelData[i].순번}`.includes(',')) {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                return alert(`${i + 1}번째 순번에 ' , '를 입력하지 않았습니다.`)
            }
        };
        // 운행시간
        const regex = /\d{2}:\d{2}~\d{2}:\d{2}/;
        for (i = 0; i < excelData.length; i++) {
            if (!regex.test(excelData[i].운행시간)) {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                return alert(`${i + 1}번째 운행시간이 형식에 맞지 않습니다.`)
            }
        };
        // 출/퇴근
        for (i = 0; i < excelData.length; i++) {
            if (excelData[i]["출/퇴근"] !== "출근" && excelData[i]["출/퇴근"] !== "퇴근") {
                excelUploadFile.value = ""
                excelUploadFileText.value = ""
                return alert(`${i + 1}번째 출/퇴근 항목이 형식에 맞지 않습니다.`)
            }
        };
        // 운행요일
        for (i = 0; i < excelData.length; i++) {
            let weekCheck = excelData[i].운행요일.replace(/\ /g, "")
            for (j = 0; j < weekCheck.length; j++) {
                if (weekCheck[j] !== "월" && weekCheck[j] !== "화" && weekCheck[j] !== "수" && weekCheck[j] !== "목" && weekCheck[j] !== "금" && weekCheck[j] !== "토" && weekCheck[j] !== "일") {
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    return alert(`${i + 1}번째 운행요일 항목이 형식에 맞지 않습니다.`)
                }
            };
        };


        visibleLoading.style.display = "block"

        let formatingData = []
        for (i = 0; i < excelData.length; i++) {
            let driveWeek = ""
            for (j = 0; j < excelData[i].운행요일.length; j++) {
                if (j == excelData[i].운행요일.length - 1) {
                    driveWeek = `${driveWeek}` + `${excelData[i].운행요일[j]}`
                } else {
                    driveWeek = `${driveWeek}` + `${excelData[i].운행요일[j]}` + " "
                }
            };
            let nembering = excelData[i].순번.replace(/\ /g, "")

            let formatingObj = {
                group: excelData[i].그룹,
                route: excelData[i].노선명,
                departure: excelData[i].출발지,
                arrival: excelData[i].도착지,
                number1: nembering.split(",")[0],
                number2: nembering.split(",")[1],
                departure_time: excelData[i].운행시간.split("~")[0],
                arrival_time: excelData[i].운행시간.split("~")[1],
                work_type: excelData[i]["출/퇴근"],
                location: excelData[i].위치 == undefined ? "" : excelData[i].위치,
                week: driveWeek,
                detailed_route: excelData[i].상세노선 == undefined ? "" : excelData[i].상세노선,
                price: excelData[i].금액,
                driver_allowance: excelData[i].기사수당,
                references: excelData[i].참조사항 == undefined ? "" : excelData[i].참조사항,
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
                if (data['group_error']) {
                    alert(`${data['line']}번째 그룹 항목 ${data['group_error']} 가 그룹목록에 존재하지 않습니다.`)
                    excelUploadFile.value = ""
                    excelUploadFileText.value = ""
                    return;
                } else if (data['count']) {
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