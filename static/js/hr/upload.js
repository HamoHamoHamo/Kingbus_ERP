const uploadBtn = document.querySelector(".member-upload")
const uploadFile = document.querySelector(".uploadFile")
const uploadFileText = document.querySelector(".uploadFileText")
const uploadLicenseFile = document.querySelector(".uploadLicenseFile")
const uploadLicenseFileText = document.querySelector(".uploadLicenseFileText")
const uploadDriverLicenseFile = document.querySelector(".uploadDriverLicenseFile")
const uploadDriverLicenseFileText = document.querySelector(".uploadDriverLicenseFileText")
const uploadDeleteBtn = document.querySelectorAll(".uploadDeleteBtn")
const saveUpload = document.querySelector(".saveUpload")

uploadBtn.addEventListener("click", openUploadPopup)

function openUploadPopup() {
    popupAreaModules[2].style.display = "block"
}

let excelData = ""

function readExcel() {

    uploadFileText.value = uploadFile.files[0].name

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
            console.log(JSON.stringify(rows));
        })
    };
    reader.readAsBinaryString(input.files[0]);
}

uploadLicenseFile.addEventListener("change", uploadLicense)

function uploadLicense() {
    uploadLicenseFileText.value = uploadLicenseFile.files[0].name
}

uploadDriverLicenseFile.addEventListener("change", uploadDriverLicense)

function uploadDriverLicense() {
    uploadDriverLicenseFileText.value = uploadDriverLicenseFile.files[0].name
}

uploadDeleteBtn[0].addEventListener("click", deleteUpload)
uploadDeleteBtn[1].addEventListener("click", deleteUpload1)
uploadDeleteBtn[2].addEventListener("click", deleteUpload2)

function deleteUpload() {
    uploadFileText.value = ""
    uploadFile.value = ""
}
function deleteUpload1() {
    uploadLicenseFileText.value = ""
    uploadLicenseFile.value = ""
}
function deleteUpload2() {
    uploadDriverLicenseFileText.value = ""
    uploadDriverLicenseFile.value = ""
}

saveUpload.addEventListener("click", dateFormat)

function dateFormat(){
    let formatingData = []
    for (i = 0; i < excelData.length; i++){
        let formatingObj = {
            name : excelData[i].이름,
            role : excelData[i].담당업무,
            entering_date : excelData[i].입사일 === undefined ? "" : excelData[i].입사일.substr(0,10),
            phone_num : excelData[i].휴대폰번호,
            birthdate : excelData[i].생년월일.substr(0,10),
            address : excelData[i].주소 === undefined ? "" : excelData[i].주소,
            note : excelData[i].비고 === undefined ? "" : excelData[i].비고,
            user_id : excelData[i].아이디 === undefined ? "" : excelData[i].아이디
        }
        formatingData.push(formatingObj)
    };
    let formatingLicense = uploadLicenseFile.files
    let formatingDriverLicense = uploadDriverLicenseFile.files
    
    console.log(formatingData);

    // $.ajax({
    //     url: "/dispatch/order/route/edit/check",
    //     method: "POST",
    //     data: {
    //         "excel": formatingData,
    //         "license": formatingLicense,
    //         "driverLicense": formatingDriverLicense,
    //         'csrfmiddlewaretoken': csrftoken
    //     },
    //     datatype: 'json',
    //     success: function (data) {
    //         if (data['status'] == "failName") {
    //             alert("등록실패 : 중복된 이름이 있습니다.")
    //             return;
    //         }else if(data['status'] == "failId"){
    //             alert("등록실패 : 중복된 아이디가 있습니다.")
    //         } else {
    //             if(confirm(`${"데이터개수"}개의 데이터를 저장하시겠습니까?`)){
    //                 inputDispatchForm.submit();
    //             // alert으로 등록에 실패한 이미지 알려주기
    //             }
    //         }
    //     },
    //     error: function (request, status, error) {
    //         console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
    //     },
    // });
}